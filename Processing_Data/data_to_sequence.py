import os
import pandas as pd
import numpy as np
import h5py

class DataProcessor:
    def __init__(self, participant_id, file_path, sampling_rate=64, sequence_duration=600, day_limit=None):
        """
        Initialize the DataProcessor class.

        Parameters:
        - participant_id: int, the ID of the participant.
        - file_path: str, path to the directory containing CSV files.
        - sampling_rate: int, the sampling rate in Hz.
        - sequence_duration: int, duration of each sequence in seconds.
        - day_limit: int or None, maximum number of days to process (default is None, meaning all days).
        """
        self.participant_id = participant_id
        self.file_path = file_path
        self.sampling_rate = sampling_rate
        self.sequence_duration = sequence_duration
        self.sequence_length = sampling_rate * sequence_duration  # Number of samples per sequence
        self.day_limit = day_limit

    def read_data(self, day):
        """
        Reads a single day's data from a CSV file.
        """
        file = fr'{self.file_path}\Participant{self.participant_id}-Day{day}.csv'
        return pd.read_csv(file)

    def process_day_data(self, df, day):
        """
        Processes data for a single day, yielding sequences and timestamps.
        """
        num_samples = len(df)
        num_sequences = num_samples // self.sequence_length  # Number of complete sequences
        print(f"Processing Day {day} - Number of sequences: {num_sequences}")

        df['Time'] = pd.to_timedelta(df['Time']).astype('int64')

        for i in range(num_sequences):
            start_idx = i * self.sequence_length
            end_idx = (i + 1) * self.sequence_length

            # # Extract one sequence of data
            sequence = df.iloc[start_idx:end_idx].to_numpy().T  # Transpose to (num_features, sequence_length)
            # sequence = df.drop(columns=['Time']).iloc[start_idx:end_idx].to_numpy().T  # Transpose to (num_features, sequence_length)

            # Extract start and end timestamps
            start_time = df['Time'].iloc[start_idx]
            end_time = df['Time'].iloc[end_idx - 1]

            yield sequence, (start_time, end_time)

    def combine_all_data(self):
        """
        Combines all processed data and timestamps across all days.
        """
        all_sequences = []
        all_timestamps = []

        # Iterate through all available days
        num_files = len([file for file in os.listdir(self.file_path) if file.endswith(".csv")])

        # Apply day limit if provided
        days_to_process = num_files if self.day_limit is None else min(self.day_limit, num_files)
        print(f"Processing {days_to_process} days out of {num_files} available days.")

        for day in range(1, days_to_process + 1):
            df = self.read_data(day)
            # df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S.%f').view('int64')  # Convert Time to datetime

            # Process data for the current day
            for sequence, timestamps in self.process_day_data(df, day):
                all_sequences.append(sequence)
                all_timestamps.append(timestamps)

        # Convert to NumPy arrays
        all_data_array = np.stack(all_sequences, axis=0)  # Shape: (total_sequences, num_features, sequence_length)
        all_timestamps_array = np.array(
            all_timestamps,
            dtype=[('start', 'int64'), ('end', 'int64')]  # Store as int64
        )

        return all_data_array, all_timestamps_array

    def save_to_h5py(self, all_data_array, all_timestamps_array, output_file):
        """
        Saves the data and timestamps to an HDF5 file.
        """
        with h5py.File(output_file, 'w') as h5file:
            h5file.create_dataset('data', data=all_data_array, compression='gzip', compression_opts=9)
            
            # Save start and end times as integers
            h5file.create_dataset('timestamps/start', data=all_timestamps_array['start'], compression='gzip', compression_opts=9)
            h5file.create_dataset('timestamps/end', data=all_timestamps_array['end'], compression='gzip', compression_opts=9)

        print(f"Data saved to {output_file}")

# Example usage (if running as a standalone script)
if __name__ == "__main__":
    participant_id = 13
    file_path = f'E:\Datasets\Canada_Dataset\Participant{participant_id}'
    output_file = fr'D:\Rainbow_DQN_Test\Test_DQN\Data\Process_canada_data\P{participant_id}_days_sequences.h5'

    processor = DataProcessor(participant_id, file_path, day_limit=None)
    all_data_array, all_timestamps_array = processor.combine_all_data()
    processor.save_to_h5py(all_data_array, all_timestamps_array, output_file)

    print(f"Total number of sequences: {all_data_array.shape}")
    print(f"Shape of one sequence: {all_data_array[0].shape}")  # (num_features, sequence_length)
    print(f"Total number of timestamps: {len(all_timestamps_array)}")
