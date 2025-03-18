import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, Subset
import numpy as np

# ---- HYPERPARAMETERS ----
BATCH_SIZE = 16
EPOCHS = 20
LEARNING_RATE = 0.001
HIDDEN_SIZE = 64
NUM_LAYERS = 2
INPUT_SIZE = 13   # Number of input features
OUTPUT_SIZE = 10  # Number of output features

# ---- GENERATE FAKE DATA ----
num_samples = 1000
seq_length = 120

np.random.seed(42)
X_data = np.random.rand(num_samples, seq_length, INPUT_SIZE).astype(np.float32)  # Input sequences
Y_data = np.random.rand(num_samples, seq_length, OUTPUT_SIZE).astype(np.float32)  # Ground truth labels

# ---- CONVERT TO TENSORS ----
X_tensor = torch.tensor(X_data, dtype=torch.float32)
Y_tensor = torch.tensor(Y_data, dtype=torch.float32)

# ---- CREATE TENSOR DATASET ----
dataset = TensorDataset(X_tensor, Y_tensor)

# ---- SEQUENTIAL SPLIT (NO SHUFFLING) ----
train_size = int(0.7 * len(dataset))  # 70% train
val_size = int(0.2 * len(dataset))    # 20% validation
test_size = len(dataset) - train_size - val_size  # 10% test

train_dataset = Subset(dataset, range(0, train_size))  # First 70%
val_dataset = Subset(dataset, range(train_size, train_size + val_size))  # Next 20%
test_dataset = Subset(dataset, range(train_size + val_size, len(dataset)))  # Last 10%

# ---- CREATE DATALOADERS ----
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=False)  # No shuffle
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

# ---- STATEFUL LSTM ENCODER-DECODER MODEL ----
class Stateful_LSTM_Seq2Seq(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(Stateful_LSTM_Seq2Seq, self).__init__()

        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # Encoder
        self.encoder = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)

        # Decoder
        self.decoder = nn.LSTM(hidden_size, hidden_size, num_layers, batch_first=True)
        self.fc_out = nn.Linear(hidden_size, output_size)

    def forward(self, x, encoder_hidden, decoder_hidden, target_seq=None, teacher_forcing_ratio=0.5):
        """
        x: (batch_size, seq_len, input_size)
        encoder_hidden: Tuple (h_0, c_0) from previous batch
        decoder_hidden: Tuple (h_0, c_0) for decoder
        target_seq: (batch_size, seq_len, output_size) - Used for teacher forcing
        """
        batch_size, seq_len, _ = x.shape
        device = x.device

        # ---- ENCODER ----
        _, encoder_hidden = self.encoder(x, encoder_hidden)

        # ---- DECODER ----
        target_seq_len = target_seq.shape[1] if target_seq is not None else seq_len
        decoder_input = torch.zeros(batch_size, 1, self.hidden_size).to(device)  # Start token

        outputs = []
        for t in range(target_seq_len):
            decoder_output, decoder_hidden = self.decoder(decoder_input, decoder_hidden)
            output_t = self.fc_out(decoder_output)  # (batch_size, 1, output_size)
            outputs.append(output_t)

            # ---- TEACHER FORCING ----
            if target_seq is not None and torch.rand(1).item() < teacher_forcing_ratio:
                decoder_input = target_seq[:, t:t+1, :]
            else:
                decoder_input = output_t

        outputs = torch.cat(outputs, dim=1)  # (batch_size, seq_len, output_size)

        # ---- DETACH HIDDEN STATES ----
        encoder_hidden = (encoder_hidden[0].detach(), encoder_hidden[1].detach())
        decoder_hidden = (decoder_hidden[0].detach(), decoder_hidden[1].detach())

        return outputs, encoder_hidden, decoder_hidden

# ---- DEVICE SETUP ----
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = Stateful_LSTM_Seq2Seq(INPUT_SIZE, HIDDEN_SIZE, NUM_LAYERS, OUTPUT_SIZE).to(device)

# ---- LOSS FUNCTION & OPTIMIZER ----
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# ---- TRAINING FUNCTION ----
def train_model():
    model.train()
    for epoch in range(EPOCHS):
        total_loss = 0
        encoder_hidden = None
        decoder_hidden = None

        for X_batch, Y_batch in train_loader:
            X_batch, Y_batch = X_batch.to(device), Y_batch.to(device)

            # ---- INITIALIZE HIDDEN STATE ----
            if encoder_hidden is None:
                encoder_hidden = (torch.zeros(NUM_LAYERS, BATCH_SIZE, HIDDEN_SIZE).to(device),
                                  torch.zeros(NUM_LAYERS, BATCH_SIZE, HIDDEN_SIZE).to(device))
            if decoder_hidden is None:
                decoder_hidden = encoder_hidden

            optimizer.zero_grad()
            outputs, encoder_hidden, decoder_hidden = model(X_batch, encoder_hidden, decoder_hidden, Y_batch, teacher_forcing_ratio=0.5)
            loss = criterion(outputs, Y_batch)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_train_loss = total_loss / len(train_loader)

        # ---- VALIDATION ----
        model.eval()
        with torch.no_grad():
            val_loss = 0
            for X_val_batch, Y_val_batch in val_loader:
                X_val_batch, Y_val_batch = X_val_batch.to(device), Y_val_batch.to(device)
                val_outputs, _, _ = model(X_val_batch, encoder_hidden, decoder_hidden, Y_val_batch, teacher_forcing_ratio=0)
                val_loss += criterion(val_outputs, Y_val_batch).item()
            avg_val_loss = val_loss / len(val_loader)

        print(f"Epoch [{epoch+1}/{EPOCHS}] - Train Loss: {avg_train_loss:.4f} - Val Loss: {avg_val_loss:.4f}")

# ---- STATEFUL TEST FUNCTION ----
def test_model():
    model.eval()
    test_loss = 0
    encoder_hidden = None  # Track hidden state across batches
    decoder_hidden = None

    with torch.no_grad():
        for X_test_batch, Y_test_batch in test_loader:
            X_test_batch, Y_test_batch = X_test_batch.to(device), Y_test_batch.to(device)

            # ---- If first batch, initialize hidden state ----
            if encoder_hidden is None:
                encoder_hidden = (torch.zeros(NUM_LAYERS, BATCH_SIZE, HIDDEN_SIZE).to(device),
                                  torch.zeros(NUM_LAYERS, BATCH_SIZE, HIDDEN_SIZE).to(device))
            if decoder_hidden is None:
                decoder_hidden = encoder_hidden

            # ---- Forward Pass (Stateful) ----
            test_outputs, encoder_hidden, decoder_hidden = model(X_test_batch, encoder_hidden, decoder_hidden, Y_test_batch, teacher_forcing_ratio=0)

            # ---- Compute Loss ----
            test_loss += criterion(test_outputs, Y_test_batch).item()

    avg_test_loss = test_loss / len(test_loader)
    print(f"\nFinal Test Loss: {avg_test_loss:.4f}")


# ---- RUN TRAINING & TESTING ----
train_model()
test_model()
