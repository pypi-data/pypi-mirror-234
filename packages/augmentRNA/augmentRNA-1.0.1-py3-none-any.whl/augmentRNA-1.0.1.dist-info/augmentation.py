import tqdm
import time
import pickle as pk
from pathlib import Path
import pandas as pd
import polars as pl
import sys
from sklearn.utils import shuffle
import numpy as np
import statistics
from scipy.stats import nbinom
from multiprocessing.pool import ThreadPool as Pool

def normalize_data(data, polars = False, round_data = True):
    '''
    Inputs
    --------
    data : polars df, pandas df
        Input dataframe to normalize
    
    polars : bool
        Whether a polars dataframe (True) or pandas dataframe (False) should be used

    round_data : bool
        Whether the output values should be converted to integers or kept as floats

    Outputs
    --------
    data : polars df, pandas df
        Output normalized dataframe
    '''

    data_columns = data.columns

    if polars == True:
        read_counts = []
        for row in data.iter_rows():
            read_counts.append(sum(row[:-1]))
    
        read_mean = sum(read_counts)/len(read_counts)
        read_multipliers = [read/read_mean for read in read_counts]
        normal_data = []
        for num, row in enumerate(data.iter_rows()):
            multiplier = read_multipliers[num]
            normal = [int(i * multiplier) for i in row[:-1]] + [row[-1]]
            normal_data.append(normal)
        data = pl.DataFrame(normal_data, schema = data_columns)
        if round_data == True:
            data = data.astype(pl.Int64)
    else:
        read_counts = []
        print(data)
        for row in data.iterrows():
            read_counts.append(sum(list(row)[:-1]))
    
        read_mean = sum(read_counts)/len(read_counts)
        read_multipliers = [read/read_mean for read in read_counts]
        normal_data = []
        for num, row in enumerate(data.iterrows()):
            multiplier = read_multipliers[num]
            normal = [int(i * multiplier) for i in row[:-1]] + [row[-1]]
            normal_data.append(normal)
        data = pd.DataFrame(normal_data, columns = data_columns, ignore_index = True)
        if round_data == True:
            data = data.astype('int64')
        
    return data

def augment_data(data, num_samples, label = 'RA', selected_label = 0, evals = False, epochs = 20,
                  augment_type = 'nbinom', polars = False, normalize = False, noise = 0):
    '''
    Augments new data samples for RNA-seq analysis

    Inputs
    -------------------------
    data : polars df, pandas df, str
        A dataframe containing the RNA-seq data, or a path to a .csv file of the dataframe

    num_samples : int
        The additional numbers of samples that should be augmented from the data

    label : str
        The label of the df column containing the classification label

    selected_label : str, int
        The selected label that should be amplified. 'all' will amplify all labels to the selected amount

    noise : float, int
        The amount of noise that should be applied to the data. A randomly selected value from the minimum and the maximum
        of the select gene column will be chosen them multiplied by the "noise" variable from -noise to noise, which will 
        then be added to the data.

    augment_type : str
        The type of augmentation that should be performed. A string containing 'nbinom' will sample from negative binomial  
        where applicable, otherwise sampling from a normal distribution, or for genes with no expression in the sample, will 
        just output zeroes. A string containing 'gan' will sample from a generative adversarial network to generate samples.
        Defaults to nbinom

    evals : bool
        Whether or not the mean squared error for each read count column should be calculated. Defaults to False

    polars : bool
        Whether a polars (True) or pandas dataframe (False) should be used as the input dataframe. Defaults to False

    normalize_data : bool
        Whether the data should be normalized based on read counts. Defaults to False

    epochs : int
        If a GAN is generated, how many epochs should the model be run for? Defaults to 20

    Outputs
    ---------------
    data : polars df, pandas df
        Output dataframe containing augmented data and old data

    '''
    if polars == True:  
        try:
            data = pl.read_csv(data)
        except:
            pass

        if selected_label != 'all':
            selected_data = data.filter(pl.col(label) == selected_label).drop(label)
            length = len(selected_data)
        else:
            labels = data[label].to_list()
            label_counts = {}
            for l in labels:
                try:
                    label_counts[l] += 1
                except: 
                    label_counts[l] = 1
            length = len(data)
    else:
        try:
            data = pd.read_csv(data)
        except:
            pass

        if selected_label != 'all':
            selected_data = data[data[label] == selected_label]
            length = len(selected_data)
        else:
            labels = list(data[label])
            label_counts = {}
            for l in labels:
                try:
                    label_counts[l] += 1
                except: 
                    label_counts[l] = 1
            length = len(data)

    data_columns = data.columns
    start = time.perf_counter()

    # If enabled, performs normalization of the data
    if normalize == True:
        data = normalize_data(data, round_data = False, polars = polars)
            
    if augment_type.upper() == 'NBINOM':

        def augment_genes(column, data = data, samples = num_samples):
            exp = data[column]
            mean = exp.sum() / length
            if mean > 0:
                var = statistics.variance(exp)
                try:
                    k = (mean ** 2) / (var - mean)
                    if k <= 0:
                        std = statistics.stdev(exp)
                        generated_values = np.rint(np.random.normal(mean, std, samples))#.astype(np.int64)
                        if noise != 0:
                            noisy = []
                            for count, sample in enumerate(generated_values):
                                noisy.append(sample + (noise * sample * random.uniform(-1, 1)))
                            generated_values = np.rint([i if i < 0 else 0 for i in noisy])
                        
                    else:
                        p = k / (k + mean)
                        generated_values = np.rint(nbinom.rvs(n=k, p=p, size=samples))#.astype(np.int64)
                        if noise != 0:
                            noisy = []
                            for count, sample in enumerate(generated_values):
                                noisy.append(sample + (noise * sample * random.uniform(-1, 1)))
                            generated_values = np.rint([i if i < 0 else 0 for i in noisy])
                    
                except:
                    std = statistics.stdev(exp)
                    generated_values = np.rint(np.random.normal(mean, std, samples))#.astype(np.int64)
                    if noise != 0:
                        noisy = []
                        for count, sample in enumerate(generated_values):
                            noisy.append(sample + (noise * sample * random.uniform(-1, 1)))

                        generated_values = np.rint([i if i < 0 else 0 for i in noisy])
                generated_values = list(generated_values)
            else:
                generated_values = [0 for _ in range(samples)]

            return generated_values

        if selected_label != 'all':
            augmented_data = {}
            for column in tqdm.tqdm(data_columns, total = len(data_columns), 
                                    desc = f'Augmenting {num_samples} genes for label {selected_label}'):
                augmented = augment_genes(column)
                augmented_data[column] = augmented

            if polars == True:
                augmented_labels = pd.DataFrame.from_dict({label:[selected_label for _ in range(num_samples)]})
            else:
                augmented_labels = pl.DataFrame({label:[selected_label for _ in range(num_samples)]})

        else:
            label_dict = {}
            augmented_data = {i:[] for i in data_columns[:-1]}
            sample_length = int(num_samples / len(list(set(label_counts.keys()))))
            for chosen_label in list(set(label_counts.keys())):
                remaining_samples =  sample_length - list(data[label]).count(chosen_label)
                label_dict[chosen_label] = remaining_samples

                if polars == True:
                    selected_data = data.filter(pl.col(label) == chosen_label).drop(label)
                else: 
      
                    selected_data = data[data[label] == chosen_label]
                    selected_data = selected_data.drop(columns = label)

                for column in tqdm.tqdm(data_columns[:-1], total = len(data_columns) - 1,
                                         desc = f'Augmenting {remaining_samples} genes for label {chosen_label}'):
                    augmented = augment_genes(column, data = selected_data, samples = remaining_samples)
                    augmented_data[column] += augmented

            augmented_labels = [key for key, value in label_counts.items() for _ in range(value)]
        
            if polars == True:
                augmented_labels = pl.DataFrame({label:augmented_labels})
            else:
                augmented_labels = pd.DataFrame.from_dict({label:augmented_labels})
            
        # Evaluates for accurracy 
        if evals == True: 
            means = []
            for column in range(data.shape[1]):
                test = data[:, column].to_list()
                evaluate = augmented_data[data_columns[column]]
                test_mean = sum(test)/len(test)
                eval_mean = sum(evaluate)/len(evaluate)
                try:
                    mean = pow(test_mean - eval_mean, 2)
                except:
                    mean = 0
                means.append(mean)
            mean_deviation = sum(means)/len(means)
            print(f'MSE deviation: {mean_deviation}')

        augmented_data = {key:np.array(value).astype(np.int64) for key, value in augmented_data.items()}
    
        if polars == True:
            augmented_data = pl.concat([pl.DataFrame(augmented_data), augmented_labels], how = "horizontal")
            columns, aug_numpy = augmented_data.columns, np.rint(augmented_data.to_numpy())
            augmented_data = pl.DataFrame(aug_numpy, schema = columns)
            data_numpy = np.rint(data.to_numpy())
            data = pl.DataFrame(data_numpy, schema = columns)
            data = pl.concat([data, augmented_data], how = "vertical")

        else:
            augmented_data = pd.concat([
                pd.DataFrame(augmented_data), 
                augmented_labels
            ], axis=1, ignore_index=False).astype('int64')
            data = data.astype('int64')
            data = pd.concat([data, augmented_data], axis = 0)
        
    elif augment_type.upper() == 'GAN':
        try:
            from torch import nn
            import torch
            import torch.optim as optim
            from sklearn.preprocessing import StandardScaler, normalize
        except:
            print('GAN functionality requires torch and sklearn! Install them with pip install torch and pip install sklearn')
            sys.exit()

        # Define the Generator and Discriminator classes
        class Generator(nn.Module):
            def __init__(self, input_size, hidden_size, output_size):
                super(Generator, self).__init__()
                self.model = nn.Sequential(
                    nn.Linear(input_size, hidden_size),
                    nn.ReLU(),
                    nn.Linear(hidden_size, output_size),
                )
        
            def forward(self, x):
                return self.model(x)
        
        class Discriminator(nn.Module):
            def __init__(self, input_size, hidden_size, output_size):
                super(Discriminator, self).__init__()
                self.model = nn.Sequential(
                    nn.Linear(input_size, hidden_size * 10),
                    nn.ReLU(),
                    nn.Linear(hidden_size * 10, hidden_size),
                    nn.ReLU(),
                    nn.Linear(hidden_size, output_size),
                )
        
            def forward(self, x):
                return self.model(x)
            
        if selected_label != 'all':
            if polars != True:
                norm = data.filter(pl.col(label) == selected_label).drop(label)
            else:
                norm = data[data[label] == selected_label].drop(label)
            X = norm.to_numpy()
            input_size = X.shape[1] 
            scaler = StandardScaler()
            X = scaler.fit_transform(X)

        else:
            selected_X = {}
            scalers = {}
            sample_numbers = {}
            labels = list(set(data[label]))
            sample_subset = int(num_samples/len(labels))

            if polars != True:
                
                for chosen_label in labels:
                    sample_numbers[chosen_label] = sample_subset - list(data[label]).count(chosen_label)
                    selected_X[chosen_label] =  data[data[label] == chosen_label].drop(label).to_numpy()
                    input_size = selected_X[chosen_label].shape[1] 
                    scaler = StandardScaler()
                    selected_X[chosen_label] = scaler.fit_transform(selected_X[chosen_label])
                    scalers[chosen_label] = scaler
                    
            else:
                for chosen_label in labels:
 
                    sample_numbers[chosen_label] = sample_subset - list(data[label]).count(chosen_label)
                    selected_X[chosen_label] = data.filter(pl.col(label) == chosen_label).drop(label).to_numpy()
                    input_size = selected_X[chosen_label].shape[1] 
                    scaler = StandardScaler()
                    selected_X[chosen_label] = scaler.fit_transform(selected_X[chosen_label])
                    scalers[chosen_label] = scaler

        hidden_size, output_size, batch_size = 256, 1, 50        
        G_lr, D_lr = 0.0002, 0.001               # Learning rate for the discriminator
        num_epochs = epochs          # Number of training epochs
        clip_value = 0.001           # Clip parameter for weight clipping (WGAN-specific)
        
        # Initialize networks
        generator = Generator(input_size, hidden_size, input_size)  # Output size matches input size
        discriminator = Discriminator(input_size, hidden_size, output_size)
        
        # Loss function and optimizers
        optimizer_G = optim.RMSprop(generator.parameters(), lr=G_lr, weight_decay = .001)
        optimizer_D = optim.RMSprop(discriminator.parameters(), lr=D_lr, weight_decay = .001)
        
        def run_model(X, input_scaler, samples = num_samples, chosen_label = selected_label):
            for epoch in tqdm.tqdm(range(num_epochs), total = num_epochs, desc = f'Training GAN to generate {samples} samples of label {chosen_label}'):
                for i in range(0, X.shape[0], batch_size):
                    # Sample real data
                    real_data = torch.tensor(X[i:i+batch_size], dtype=torch.float32)
                    
                    # Sample noise for generator
                    gen_noise = torch.randn(batch_size, input_size)
                    
                    # Generate fake data from noise
                    fake_data = generator(gen_noise)
                    
                    # Discriminator forward and backward pass
                    optimizer_D.zero_grad()
                    
                    # Compute the discriminator scores for real and fake data
                    real_scores = discriminator(real_data)
                    fake_scores = discriminator(fake_data)
                    
                    # Compute the Wasserstein loss
                    loss_D = -torch.mean(real_scores) + torch.mean(fake_scores)
                    loss_D.backward()
                    
                    fake_data, real_scores, fake_scores = fake_data.detach(), real_scores.detach(), fake_scores.detach()
                
                    # Weight clipping (WGAN-specific)
                    for param in discriminator.parameters():
                        param.data.clamp_(-clip_value, clip_value)
                    
                    # Update discriminator
                    optimizer_D.step()
                    
                    # Generator forward and backward pass
                    optimizer_G.zero_grad()
                
                    # Compute the discriminator scores for fake data (detach to avoid backpropagation)
                    fake_scores = discriminator(fake_data)
                
                    # Compute the generator loss
                    loss_G = -torch.mean(fake_scores)
                
                    loss_G.backward()
                
                    # Update generator
                    optimizer_G.step()
                
                # Print progress
                if epoch == num_epochs - 1 and evals == True:
                    print(f"Wasserstein Loss (D): {loss_D.item():.4f}, Wasserstein Loss (G): {loss_G.item():.4f}")
            
            # Generate fake samples
            generated_noise = torch.randn(samples, input_size)
            faked_samples = input_scaler.inverse_transform(generator(generated_noise).detach().numpy())

            if noise > 0:
                for column in range(faked_samples.shape[1]):
                    col = faked_samples[:, column]
    
                    noisy = []
                    for count, sample in enumerate(col):
                        noisy.append(sample + (noise * sample * random.uniform(-1, 1)))
                    faked_samples[:, column] = np.rint(noisy)
        
            labels = np.array([chosen_label for _ in range(samples)]).reshape(-1, 1)
    
            fake_samples = np.hstack((np.rint(faked_samples), labels))

            return fake_samples
        
        if selected_label != 'all':
            fake_samples = run_model(X, input_scaler = scaler)
        else:
            for chosen_label in labels:
                scaler = scalers[chosen_label]
                X = selected_X[chosen_label]

                print(sample_numbers[chosen_label])
                faked = run_model(X, input_scaler = scaler, chosen_label = chosen_label, samples = sample_numbers[chosen_label] )
        
                try:
                    fake_samples = np.vstack((fake_samples, faked))
                except:
                    fake_samples = faked

        if polars == True:
            fake_samples = pl.DataFrame(fake_samples, schema = data_columns)
            data = pl.concat((data, fake_samples), how = "vertical")
            data = data.sample(fraction = 1.0, shuffle = True)
        else:
            fake_samples = pd.DataFrame(fake_samples, columns = data_columns)
            data = pd.concat([data, fake_samples], axis = 0)

        # Evaluates for accurracy 
        if evals == True: 
            means = []
            for column in range(norm.shape[1]):
                test = norm[:, column].to_list()
                evaluate = faked_samples[:, column].flatten()
                test_mean = sum(test)/len(test)
                eval_mean = sum(evaluate)/len(evaluate)
                try:
                    mean = pow(test_mean - eval_mean, 2)
                except:
                    mean = 0
                means.append(mean)
            mean_deviation = sum(means)/len(means)
            print(f'MSE deviation: {mean_deviation}')
            
    end = time.perf_counter()
    print(f'{num_samples} samples augmented in {round(end - start, 4)} seconds')

    return data

def relevant_genes(data, label = 'RA', polars = False):
    '''
    Filters dataset to only contain genes that have non-zero values in all columns, or zero vaues in all columns for every label.
    Seeks to minimize bias from different sequencing/sampling methods for different labels, and make the training dataset more representative.
    
    Inputs
    -------------
    data : polars df, pandas df, str
        RNA-seq expresison dataframe

    label : str
        Dataframe column containing labels

    polars : bool
        Whether pandas (False) or polars (True) dataframe is the input 

    Outputs
    ---------------
    data : polars df, pandas df
        An output dataframe containing only genes that are relevant across all samples
    '''
    try:
        if polars == True:
            data = pl.read_csv(data)
        else:
            data = pd.read_csv(data)
    except:
        pass

    selected_genes = []
    genes = data.columns
    mean_statistics = []
   
    labels = list(set(data[label]))
    label_length = len(labels)

    for count, chosen_label in enumerate(labels):
        if polars == True:
            subset = data.filter(pl.col(label) == chosen_label)
        else:
            subset = data[data[label] == chosen_label]

        for num, column in enumerate(genes):
            mean = sum(subset[column]/len(subset[column]))
            if count == 0:
                mean_statistics.append([mean])
            else:
                mean_statistics[num].append(mean)
               
    for count, stat in enumerate(mean_statistics):

        if 0 in stat:
            if stat.count(0) == label_length:
                selected_genes.append(genes[count])
        else:
            selected_genes.append(genes[count])
        
    if polars != True:
        data = data[selected_genes]
    else:
        data = data.select(selected_genes)

    print(f'{len(mean_statistics)} trimmed down to {len(data.columns)} relevant genes')
    return data

if __name__ == '__main__':
    data = relevant_genes(Path('/work/ccnr/GeneFormer/GeneFormer_repo/Enzo_dataset.csv'))
    data = augment_data(Path('/work/ccnr/GeneFormer/GeneFormer_repo/Enzo_dataset.csv'), polars = True,
                        num_samples = 4200, selected_label = 'all', normalize = False, augment_type = 'GAN')