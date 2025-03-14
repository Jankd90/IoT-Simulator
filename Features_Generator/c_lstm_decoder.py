import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset, Subset
import optuna
import numpy as np
import h5py
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import math

import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, TensorDataset, random_split

# Set device 
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define the Generator Model
class Generator(nn.Module):
    def __init__(self, feature_dim, hidden_dim, condition_dim, num_layers=1, bidirectional=False):
        super(Generator, self).__init__()
        self.lstm = nn.LSTM(feature_dim + condition_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.3, bidirectional=bidirectional)
        self.fc1 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim // 2, feature_dim)
        
    def forward(self, noise, condition):
        x = torch.cat((noise, condition), dim=-1)
        output, _ = self.lstm(x)
        x = self.fc1(output)
        x = self.relu(x)
        return self.fc2(x)

# Function to generate synthetic data
def generate_data(num_samples, seq_length, feature_dim):
    noise = torch.randn(num_samples, seq_length, feature_dim)  # Random noise input
    return noise

# Function to create DataLoaders
def create_dataloaders(conditions, real_data, batch_size, train_ratio=0.7, val_ratio=0.15):
    num_samples = real_data.shape[0]
    train_size = int(train_ratio * num_samples)
    val_size = int(val_ratio * num_samples)
    test_size = num_samples - train_size - val_size

    dataset = TensorDataset(conditions, real_data)
    train_set, val_set, test_set = random_split(dataset, [train_size, val_size, test_size])

    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, test_loader

# Function to train the model
def train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs):
    train_losses, val_losses = [], []

    for epoch in range(num_epochs):
        model.train()
        train_loss = 0
        for noise_batch, cond_batch, real_batch in train_loader:
            noise_batch, cond_batch, real_batch = noise_batch.to(device), cond_batch.to(device), real_batch.to(device)

            optimizer.zero_grad()
            generated_data = model(noise_batch, cond_batch)
            loss = criterion(generated_data, real_batch)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()
            
        train_loss /= len(train_loader)
        train_losses.append(train_loss)

        # Validation phase
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for noise_batch, cond_batch, real_batch in val_loader:
                noise_batch, cond_batch, real_batch = noise_batch.to(device), cond_batch.to(device), real_batch.to(device)
                generated_data = model(noise_batch, cond_batch)
                loss = criterion(generated_data, real_batch)
                val_loss += loss.item()

        val_loss /= len(val_loader)
        val_losses.append(val_loss)

        print(f"Epoch [{epoch+1}/{num_epochs}], Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")

    return train_losses, val_losses

# Function to evaluate the model on test data
def test_model(model, test_loader, criterion):
    model.eval()
    test_loss = 0
    with torch.no_grad():
        for noise_batch, cond_batch, real_batch in test_loader:
            noise_batch, cond_batch, real_batch = noise_batch.to(device), cond_batch.to(device), real_batch.to(device)
            generated_data = model(noise_batch, cond_batch)
            loss = criterion(generated_data, real_batch)
            test_loss += loss.item()

    test_loss /= len(test_loader)
    print(f"Test Loss: {test_loss:.4f}")
    return test_loss

# Function to plot loss curves
def plot_loss(train_losses, val_losses):
    plt.plot(train_losses, label="Train Loss")
    plt.plot(val_losses, label="Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.legend()
    plt.title("Training & Validation Loss")
    plt.show()

# 5. Load Data
def load_data(file_path):
    with h5py.File(file_path, 'r') as f:
        X = f['data'][:]
    return X

# 5. Load conditions
def load_conditions(file_path):
    pass

# 1. Process Data
def process_data(X):
    data = torch.from_numpy(X).float()  # Convert to PyTorch tensor

    # Print shape to confirm it remains unchanged
    print("Original shape:", data.shape)
    return data

# 1. Process conditions
def process_conditions(C):
    conditions = torch.from_numpy(C).float()  # Convert to PyTorch tensor

    # Print shape to confirm it remains unchanged
    print("Original shape:", conditions.shape)
    return conditions

# 8. Save Model Function
def save_model(model, filepath):
    torch.save(model.state_dict(), filepath)
    print(f"Model saved to {filepath}")

# Main function
def main():
    data_file_path = fr''
    conditions_file_path = fr''

    real_data = load_data(data_file_path)
    conditions = load_conditions(conditions_file_path)

    # Hyperparameters
    feature_dim = 10  # Number of features in real data
    hidden_dim = 64  # Hidden layer size
    condition_dim = 11  # Size of conditional input
    num_epochs = 37
    batch_size = 16
    learning_rate = 0.0002305394710098038
    seq_length = 120  # Length of input sequence
    num_samples = 1000  # Total number of sequences

    # Generate Data
    noise = generate_data(num_samples, seq_length, feature_dim)

    # Create DataLoaders
    train_loader, val_loader, test_loader = create_dataloaders(conditions, real_data, batch_size)

    # Initialize model, loss function, and optimizer
    model = Generator(feature_dim, hidden_dim, condition_dim).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # Train the model
    train_losses, val_losses = train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs, batch_size)

    # Plot loss curves
    plot_loss(train_losses, val_losses)

    # Test the model
    test_loss = test_model(model, test_loader, criterion)

if __name__ == "__main__":
    main()




# # 9. Main Execution Code
# def main():
#     # Update with actual file path
#     file_path = r"D:\Ali_Thesis\synthetic_data_generation\Data\Process_canada_data\P13_5_sec_30hz_sequences_sensor_data_std_normalized.h5"
#     data = load_data(file_path)

#     # order = [1, 2, 3, 4, 5, 0]  # Acc_X, Acc_y, Acc_z, BvP, TEMP, EDA
#     X = process_data(data)
    
#     num_channels = X.shape[1]
#     hidden_size = 64
#     num_layers = 2
#     feature_dim = 10
#     batch_size = 16
#     num_epochs = 37
#     lr_g = 0.0002305394710098038

#     model = LSTM_Decoder(
#         num_channels=num_channels,
#         hidden_size=hidden_size,
#         num_layers=num_layers,
#         feature_dim=feature_dim
#     ).to(device)

#     dataset = TensorDataset(X, X)

#     # Define split sizes (e.g., 70% training, 15% validation, 15% test)
#     train_size = int(0.7 * len(dataset))

#     # Use Subset to create sequential splits
#     train_dataset = Subset(dataset, range(train_size))  # First 80% for training
#     val_dataset = Subset(dataset, range(train_size, len(dataset)))  # Last 20% for validation

#     train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False, drop_last=True)
#     val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, drop_last=True)
#     test_loader = DataLoader()

#     train_decoder(model, train_loader, val_loader, num_epochs=num_epochs, lr_g=lr_g, save_results=True)

#     test_loader()

#     save_model(model, 'feature_decoder.pth')

# if __name__ == "__main__":
#     main()
