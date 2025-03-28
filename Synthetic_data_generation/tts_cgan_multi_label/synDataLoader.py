#synthetic heartbeat signal dataloader
#generate synthetic signal from the pre-trained generator model

import numpy as np
import torch 
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from TransCGAN_model import *
from DataLoader import *

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

cls_dit = {'Non-Ectopic Beats':0, 'Superventrical Ectopic':1, 'Ventricular Beats':2,
                                                'Unknown':3, 'Fusion Beats':4}

class syn_mitbih(Dataset):
    def __init__(self, n_samples=20000, seq_len=150, channels=3, reshape=False, num_classes=10, 
                 model_path=r'D:\Hanze_Master\Thesis\Syn_data_gen\tts-cgan\logs\mitbithCGAN_2025_01_10_13_43_49\Model\checkpoint'):
        
        gen_net = Generator(seq_len=seq_len, channels=channels, num_classes=num_classes, latent_dim=100, 
                            data_embed_dim=10, label_embed_dim=10, depth=3, num_heads=5, 
                            forward_drop_rate=0.5, attn_drop_rate=0.5)
        GAN_ckp = torch.load(model_path)
        gen_net.load_state_dict(GAN_ckp['gen_state_dict'])

        # Generate synthetic data for all classes
        self.syn_data = []
        self.syn_labels = []
        for class_label in range(num_classes):
            synthetic_data = self.generate_synthetic_data(gen_net, class_label, n_samples)
            if reshape:
                synthetic_data = synthetic_data.reshape(synthetic_data.shape[0], channels, synthetic_data.shape[3])
            self.syn_data.append(synthetic_data)
            self.syn_labels.extend([class_label] * n_samples)

        # Concatenate data and labels
        self.data = np.concatenate(self.syn_data, axis=0)
        self.labels = np.array(self.syn_labels)

        print(f'data shape is {self.data.shape}')
        print(f'labels shape is {self.labels.shape}')
        for class_label in range(num_classes):
            print(f'The dataset includes {n_samples} samples of class {class_label}')

    def generate_synthetic_data(self, gen_net, classlabel, n):
        fake_noise = torch.FloatTensor(np.random.normal(0, 1, (n, 100)))
        fake_label = torch.tensor([classlabel] * n)
        fake_sigs = gen_net(fake_noise, fake_label).to('cpu').detach().numpy()
        return fake_sigs

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

# class syn_mitbih(Dataset):
#     def __init__(self, n_samples = 20000, seq_len = 150, channels=3, reshape = False, model_path=r'D:\Hanze_Master\Thesis\Syn_data_gen\tts-cgan\logs\mitbithCGAN_2025_01_10_13_43_49\Model\checkpoint'):       # model_path='./mitbih_checkpoint'
        
#         gen_net = Generator(seq_len=seq_len, channels=channels, num_classes=10, latent_dim=100, data_embed_dim=10, 
#                     label_embed_dim=10 ,depth=3, num_heads=5, 
#                     forward_drop_rate=0.5, attn_drop_rate=0.5)
#         GAN_ckp = torch.load(model_path)
#         gen_net.load_state_dict(GAN_ckp['gen_state_dict'])
        
#         # shape = n_samples, 1, 1, seq_len
#         self.syn_0 = self.generate_synthetic_data(gen_net, 0, n_samples)
#         self.syn_1 = self.generate_synthetic_data(gen_net, 1, n_samples)
#         self.syn_2 = self.generate_synthetic_data(gen_net, 2, n_samples)
#         self.syn_3 = self.generate_synthetic_data(gen_net, 3, n_samples)
#         self.syn_4 = self.generate_synthetic_data(gen_net, 4, n_samples)
        
#         # shape = n_samples, seq_len
#         if reshape:
#             self.syn_0 = self.syn_0.reshape(self.syn_0.shape[0], channels, self.syn_0.shape[3])
#             self.syn_1 = self.syn_1.reshape(self.syn_1.shape[0], channels, self.syn_1.shape[3])
#             self.syn_2 = self.syn_2.reshape(self.syn_2.shape[0], channels, self.syn_2.shape[3])
#             self.syn_3 = self.syn_3.reshape(self.syn_3.shape[0], channels, self.syn_3.shape[3])
#             self.syn_4 = self.syn_4.reshape(self.syn_4.shape[0], channels, self.syn_4.shape[3])
        
#         self.data = np.concatenate((self.syn_0, self.syn_1, self.syn_2, self.syn_3, self.syn_4), axis = 0)
#         self.labels = np.concatenate((np.array([0]*n_samples), np.array([1]*n_samples), np.array([2]*n_samples), np.array([3]*n_samples), np.array([4]*n_samples)))
            
#         print(f'data shape is {self.data.shape}')
#         print(f'labels shape is {self.labels.shape}')
#         print(f'The dataset including {n_samples} class 0, {n_samples} class 1, {n_samples} class 2, {n_samples} class 3, {n_samples} class 4')
        
#     def generate_synthetic_data(self, gen_net, classlabel, n):
#         fake_noise = torch.FloatTensor(np.random.normal(0, 1, (n, 100)))
#         fake_label = torch.tensor([classlabel] * n)
#         fake_sigs = gen_net(fake_noise, fake_label).to('cpu').detach().numpy()
#         return fake_sigs        
        
#     def __len__(self):
#         return len(self.labels)
    
#     def __getitem__(self, idx):
#         return self.data[idx], self.labels[idx]
    
class mixed_mitbih(Dataset):
    def __init__(self, X_train, y_train, real_samples = 200, syn_samples = 800):
        syn_ecg = syn_mitbih(n_samples=syn_samples, reshape=True)

        real_ecg = mitbih_train(X_train, y_train, n_samples=real_samples, oneD=True)
        # train_loader = data.DataLoader(train_set, batch_size=args.batch_size, num_workers=args.num_workers, shuffle=True)

        # real_ecg = mitbih_train(n_samples=real_samples, oneD=True)
        
        self.data = np.concatenate((syn_ecg.data, real_ecg.X_train), axis = 0)
        self.labels = np.concatenate((syn_ecg.labels, real_ecg.y_train), axis = 0)
        
        print(f'data shape is {self.data.shape}')
        print(f'labels shape is {self.labels.shape}')
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]