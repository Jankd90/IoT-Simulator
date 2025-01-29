# load mitbih dataset

import os 
import numpy as np
import pandas as pd
import sys 
from tqdm import tqdm 

import torch 
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.utils import resample

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

import h5py

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

cls_dit = {'Non-Ectopic Beats':0, 'Superventrical Ectopic':1, 'Ventricular Beats':2,
                                                'Unknown':3, 'Fusion Beats':4}


class DataProcessor:
    def __init__(self, h5_file=r'D:\Hanze_Master\Thesis\Syn_data_gen\fake_data\X30_sensor_data_5sec.h5' , dataset_name='data', label_file_1=r'D:\Hanze_Master\Thesis\Syn_data_gen\fake_data\Y_agitation.npz', label_file_2=r'D:\Hanze_Master\Thesis\Syn_data_gen\fake_data\Y.npz', test_size=0.2, random_state=42):
        self.h5_file = h5_file
        self.dataset_name = dataset_name
        self.label_file_1 = label_file_1
        self.label_file_2 = label_file_2
        self.test_size = test_size
        self.random_state = random_state

    def load_and_process_data(self):
        # Load the HDF5 file
        with h5py.File(self.h5_file, 'r') as f:
            X = f[self.dataset_name][:]
            print(f"Loaded data shape: {X.shape}")

        # Load labels
        labels_1 = np.load(self.label_file_1)
        labels_1 = labels_1['arr_0']
        print(f"Loaded labels shape: {labels_1.shape}")

        # Print unique labels and their counts
        unique_labels_1, counts_1 = np.unique(labels_1, return_counts=True)
        print("Labels: ", unique_labels_1)
        print("Counts: ", counts_1)
        print("Amount of Labels is: ", len(unique_labels_1))

        # Encode labels
        label_encoder_1 = LabelEncoder()
        Y_1 = label_encoder_1.fit_transform(labels_1)
        label_mapping_1 = dict(zip(label_encoder_1.classes_, range(len(label_encoder_1.classes_))))
        print("Label Mapping:", label_mapping_1)


        # Load labels
        labels_2 = np.load(self.label_file_2)
        labels_2 = labels_2['y']
        print(f"Loaded labels shape: {labels_2.shape}")

        # Print unique labels and their counts
        unique_labels_2, counts_2 = np.unique(labels_2, return_counts=True)
        print("Labels: ", unique_labels_2)
        print("Counts: ", counts_2)
        print("Amount of Labels is: ", len(unique_labels_2))

        # Encode labels
        label_encoder_2 = LabelEncoder()
        Y_2 = label_encoder_2.fit_transform(labels_2)
        label_mapping_2 = dict(zip(label_encoder_2.classes_, range(len(label_encoder_2.classes_))))
        print("Label Mapping:", label_mapping_2)



        # Split data into training and testing sets
        X_train, X_test, y1_train_agitation, y1_test_agitation, y2_train_activity, y2_test_activity = train_test_split(
            X, Y_1, Y_2, test_size=self.test_size, random_state=self.random_state
        )

        # Verify the shapes
        print("Training data shape:", X_train.shape)
        print("Testing data shape:", X_test.shape)
        print("Training labels shape:", y1_train_agitation.shape)
        print("Testing labels shape:", y1_test_agitation.shape)
        print("Training labels shape:", y2_train_activity.shape)
        print("Testing labels shape:", y2_test_activity.shape)

        return X_train, X_test, y1_train_agitation, y1_test_agitation, y2_train_activity, y2_test_activity, label_mapping_1, label_mapping_2


class mitbih_train(Dataset):
    def __init__(self, X_train, y_train_1, y_train_2, n_samples=50000, oneD=False):
        self.X_train = X_train
        self.y_agitation_train = y_train_1
        self.y_activity_train  = y_train_2

        num_samples = X_train.shape[2]
        num_channels = X_train.shape[1]

        # # Convert to Pandas DataFrame for resampling
        # df = pd.DataFrame(X_train.reshape(X_train.shape[0], -1))
        # df['label'] = y_train

        # # Resampling data for each class dynamically for classes 0 through 9
        # resampled_data = []
        # for label in range(10):
        #     class_data = df[df['label'] == label]
        #     if not class_data.empty:
        #         resampled_class_data = resample(class_data, n_samples=n_samples, random_state=123, replace=True)
        #         resampled_data.append(resampled_class_data)

        # # Combine resampled data
        # train_dataset = pd.concat(resampled_data)

        # # Separate features and labels
        # self.X_train = train_dataset.iloc[:, :-1].values
        # self.y_train = train_dataset['label'].values

        # # Reshape X_train back to original dimensions
        # num_samples = X_train.shape[2] if len(X_train.shape) == 3 else 1
        # num_channels = X_train.shape[1] if len(X_train.shape) == 3 else 1
        # self.X_train = self.X_train.reshape(self.X_train.shape[0], num_channels, num_samples)

        if oneD:
            # self.X_train = self.X_train.reshape(self.X_train.shape[0], 1, -1)  # Flatten samples within each channel
            self.X_train = self.X_train.reshape(self.X_train.shape[0], num_channels, num_samples)
        else:
            self.X_train = self.X_train.reshape(self.X_train.shape[0], num_channels, 1, num_samples)

        print(f'X_train shape is {self.X_train.shape}')
        print(f'y_train_1 shape is {self.y_agitation_train.shape}')
        print(f'y_train_2 shape is {self.y_activity_train.shape}')
        # for label in range(10):
        #     print(f'The dataset includes {len(train_dataset[train_dataset["label"] == label])} samples of class {label}')

    def __len__(self):
        return len(self.y_agitation_train)

    def __getitem__(self, idx):
        return self.X_train[idx], self.y_agitation_train[idx], self.y_activity_train[idx]


# class mitbih_train(Dataset):
#     def __init__(self, filename='./mitbih_train.csv', n_samples=20000, oneD=False):
#         data_train = pd.read_csv(filename, header=None)
        
#         # making the class labels for our dataset
#         data_0 = data_train[data_train[187] == 0]
#         data_1 = data_train[data_train[187] == 1]
#         data_2 = data_train[data_train[187] == 2]
#         data_3 = data_train[data_train[187] == 3]
#         data_4 = data_train[data_train[187] == 4]
        
#         data_0_resample = resample(data_0, n_samples=n_samples, 
#                                    random_state=123, replace=True)
#         data_1_resample = resample(data_1, n_samples=n_samples, 
#                                    random_state=123, replace=True)
#         data_2_resample = resample(data_2, n_samples=n_samples, 
#                                    random_state=123, replace=True)
#         data_3_resample = resample(data_3, n_samples=n_samples, 
#                                    random_state=123, replace=True)
#         data_4_resample = resample(data_4, n_samples=n_samples, 
#                                    random_state=123, replace=True)
        
#         train_dataset = pd.concat((data_0_resample, data_1_resample, 
#                                   data_2_resample, data_3_resample, data_4_resample))
        
#         self.X_train = train_dataset.iloc[:, :-1].values
#         if oneD:
#             self.X_train = self.X_train.reshape(self.X_train.shape[0], 1, self.X_train.shape[1])
#         else:
#             self.X_train = self.X_train.reshape(self.X_train.shape[0], 1, 1, self.X_train.shape[1])
#         self.y_train = train_dataset[187].values
            
#         print(f'X_train shape is {self.X_train.shape}')
#         print(f'y_train shape is {self.y_train.shape}')
#         print(f'The dataset including {len(data_0_resample)} class 0, {len(data_1_resample)} class 1, {len(data_2_resample)} class 2, {len(data_3_resample)} class 3, {len(data_4_resample)} class 4')
        
        
#     def __len__(self):
#         return len(self.y_train)
    
#     def __getitem__(self, idx):
#         return self.X_train[idx], self.y_train[idx]
    



class mitbih_test(Dataset):
    def __init__(self, X_test, y_test, n_samples=50000, oneD=False):
        # Convert to Pandas DataFrame for resampling
        df = pd.DataFrame(X_test.reshape(X_test.shape[0], -1))
        df['label'] = y_test

        # Resampling data for each class dynamically for classes 0 through 9
        resampled_data = []
        for label in range(10):
            class_data = df[df['label'] == label]
            if not class_data.empty:
                resampled_class_data = resample(class_data, n_samples=n_samples, random_state=123, replace=True)
                resampled_data.append(resampled_class_data)

        # Combine resampled data
        test_dataset = pd.concat(resampled_data)

        # Separate features and labels
        self.X_test = test_dataset.iloc[:, :-1].values
        self.y_test = test_dataset['label'].values

        # Reshape X_test back to original dimensions
        num_samples = X_test.shape[2] if len(X_test.shape) == 3 else 1
        num_channels = X_test.shape[1] if len(X_test.shape) == 3 else 1
        # self.X_test = self.X_test.reshape(self.X_test.shape[0], num_channels, num_samples)

        if oneD:
            # self.X_test = self.X_test.reshape(self.X_test.shape[0], 1, -1)  # Flatten samples within each channel
            self.X_test = self.X_test.reshape(self.X_test.shape[0], num_channels, num_samples)
        else:
            self.X_test = self.X_test.reshape(self.X_test.shape[0], num_channels, 1, num_samples)

        print(f'X_test shape is {self.X_test.shape}')
        print(f'y_test shape is {self.y_test.shape}')
        for label in range(10):
            print(f'The dataset includes {len(test_dataset[test_dataset["label"] == label])} samples of class {label}')

    def __len__(self):
        return len(self.y_test)

    def __getitem__(self, idx):
        return self.X_test[idx], self.y_test[idx]


    
# class mitbih_test(Dataset):
#     def __init__(self, filename='./mitbih_test.csv', n_samples=1000, oneD=False):
#         data_test = pd.read_csv(filename, header=None)
        
#         # making the class labels for our dataset
#         data_0 = data_test[data_test[187] == 0]
#         data_1 = data_test[data_test[187] == 1]
#         data_2 = data_test[data_test[187] == 2]
#         data_3 = data_test[data_test[187] == 3]
#         data_4 = data_test[data_test[187] == 4]
        
#         data_0_resample = resample(data_0, n_samples=n_samples, 
#                            random_state=123, replace=True)
#         data_1_resample = resample(data_1, n_samples=n_samples, 
#                                    random_state=123, replace=True)
#         data_2_resample = resample(data_2, n_samples=n_samples, 
#                                    random_state=123, replace=True)
#         data_3_resample = resample(data_3, n_samples=n_samples, 
#                                    random_state=123, replace=True)
#         data_4_resample = resample(data_4, n_samples=n_samples, 
#                                    random_state=123, replace=True)
        
#         test_dataset = pd.concat((data_0_resample, data_1_resample, 
#                                   data_2_resample, data_3_resample, data_4_resample))
        
#         self.X_test = test_dataset.iloc[:, :-1].values
#         if oneD:
#             self.X_test = self.X_test.reshape(self.X_test.shape[0], 1, self.X_test.shape[1])
#         else:
#             self.X_test = self.X_test.reshape(self.X_test.shape[0], 1, 1, self.X_test.shape[1])
#         self.y_test = test_dataset[187].values
        
#         print(f'X_test shape is {self.X_test.shape}')
#         print(f'y_test shape is {self.y_test.shape}')
#         print(f'The dataset including {len(data_0)} class 0, {len(data_1)} class 1, {len(data_2)} class 2, {len(data_3)} class 3, {len(data_4)} class 4')
        
#     def __len__(self):
#         return len(self.y_test)
    
#     def __getitem__(self, idx):
#         return self.X_test[idx], self.y_test[idx]