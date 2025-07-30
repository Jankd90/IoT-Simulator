import numpy as np
import h5py
import os

class SequenceReshaper:
    def __init__(self, sample_rate=64):
        """
        Initialize the SequenceReshaper.

        Parameters:
        - sample_rate (int): Sampling rate in Hz. Default is 64.
        """
        self.sample_rate = sample_rate

    def reshape_memmap_per_channel(self, input_filepath, output_filepath, dataset_name, segment_duration=60, temp_dir="temp"):
        """
        Reshape sequences into smaller sequences of specified duration, processing per channel using numpy.memmap.

        Parameters:
        - input_filepath (str): Path to the input .h5 file.
        - output_filepath (str): Path to the output .h5 file.
        - dataset_name (str): Name of the dataset in the input .h5 file.
        - segment_duration (int): Duration of each segment in seconds. Default is 60 seconds.
        - temp_dir (str): Directory to store temporary memmap files.
        """
        # Ensure the temp directory exists
        os.makedirs(temp_dir, exist_ok=True)

        # Open the input .h5 file and read metadata
        with h5py.File(input_filepath, 'r') as h5file:
            data_shape = h5file[dataset_name].shape
            num_channels = data_shape[1]
            num_samples_per_segment = self.sample_rate * segment_duration

            # Validate input
            if data_shape[2] % num_samples_per_segment != 0:
                raise ValueError("The number of samples in each sequence must be a multiple of the segment duration.")

            # Calculate number of output segments
            num_total_segments = data_shape[0] * (data_shape[2] // num_samples_per_segment)
            output_shape = (num_total_segments, num_samples_per_segment)

            # Create output HDF5 file and datasets
            with h5py.File(output_filepath, 'w') as output_h5:
                for channel in range(num_channels):
                    output_h5.create_dataset(
                        f"channel_{channel}",
                        shape=output_shape,
                        dtype=h5file[dataset_name].dtype,
                        compression="gzip",
                        compression_opts=9
                    )

                # Process each channel separately
                for channel in range(num_channels):
                    print(f"Processing channel {channel + 1}/{num_channels}...")
                    channel_memmap_path = os.path.join(temp_dir, f"channel_{channel}.dat")

                    # Create memmap file for reshaped channel
                    reshaped_channel = np.memmap(
                        channel_memmap_path,
                        dtype=h5file[dataset_name].dtype,
                        mode="w+",
                        shape=output_shape
                    )

                    # Process channel in chunks
                    chunk_size = 100  # Number of sequences to process at once
                    start_segment = 0
                    for start_idx in range(0, data_shape[0], chunk_size):
                        end_idx = min(start_idx + chunk_size, data_shape[0])
                        chunk = h5file[dataset_name][start_idx:end_idx, channel, :]  # Load a single channel chunk

                        # Reshape the chunk and store it in the memmap
                        reshaped_chunk = chunk.reshape((-1, num_samples_per_segment))
                        end_segment = start_segment + reshaped_chunk.shape[0]
                        reshaped_channel[start_segment:end_segment] = reshaped_chunk
                        start_segment = end_segment

                    # Save reshaped channel data into the HDF5 file
                    output_h5[f"channel_{channel}"][:] = reshaped_channel[:]

                    # Delete the temporary memmap file
                    del reshaped_channel
                    os.remove(channel_memmap_path)

        print(f"Data reshaped and saved to {output_filepath}")

# Example usage
if __name__ == "__main__":
    # Access the data from the .h5 file
    original_h5 = "D:\Rainbow_DQN_Test\Test_DQN\Data\Process_canada_data\P13_days_sequences.h5"
    reshaped_h5 = "D:\Rainbow_DQN_Test\Test_DQN\Data\Process_canada_data\P13_5_sec_sequences.h5"
    dataset_name = "data"

    # Create reshaper instance and reshape data into 5-second segments
    reshaper = SequenceReshaper(sample_rate=64)
    reshaper.reshape_memmap_per_channel(original_h5, reshaped_h5, dataset_name, segment_duration=5)
    print('Reshaping is done!')








# import numpy as np
# import h5py

# class SequenceReshaper:
#     def __init__(self, sample_rate=64):
#         """
#         Initialize the SequenceReshaper.

#         Parameters:
#         - sample_rate (int): Sampling rate in Hz. Default is 64.
#         """
#         self.sample_rate = sample_rate

#     def reshape(self, data, segment_duration=60):
#         """
#         Reshape sequences into smaller sequences of specified duration.

#         Parameters:
#         - data (numpy.ndarray): Input data with shape (num_sequences, num_channels, num_samples).
#         - segment_duration (int): Duration of each segment in seconds. Default is 60 seconds.
#         Returns:
#         - reshaped_data (numpy.ndarray): Reshaped data with shape 
#           (num_total_segments, num_channels, num_samples_per_segment).
#         """
#         # Calculate number of samples per segment
#         num_samples_per_segment = self.sample_rate * segment_duration
        
#         # Validate input
#         if data.shape[2] % num_samples_per_segment != 0:
#             raise ValueError("The number of samples in each sequence must be a multiple of the segment duration.")
        
#         sequences = data.shape[0] * (data.shape[2] // num_samples_per_segment)

#         # Reshape the data
#         reshaped_data = data.reshape(sequences, data.shape[1], num_samples_per_segment)
#         return reshaped_data
    
#     def read_h5(self, filepath, dataset_name):
#         """
#         Read data from an .h5 file.

#         Parameters:
#         - filepath (str): Path to the .h5 file.
#         - dataset_name (str): Name of the dataset to read.

#         Returns:
#         - data (numpy.ndarray): Loaded data.
#         """
#         with h5py.File(filepath, 'r') as h5file:
#             data = h5file[dataset_name][:]
#         return data

#     def save_h5(self, filepath, dataset_name, data):
#         """
#         Save data to an .h5 file.

#         Parameters:
#         - filepath (str): Path to the .h5 file.
#         - dataset_name (str): Name of the dataset to save.
#         - data (numpy.ndarray): Data to save.
#         """
#         with h5py.File(filepath, 'w') as h5file:
#             h5file.create_dataset('data', data=data, compression='gzip', compression_opts=9)
#         print(f"Data saved to {filepath} under dataset '{dataset_name}'")

# # Example usage
# if __name__ == "__main__":
    
#     # Access the data from the .h5 file
#     original_h5 = "D:\Rainbow_DQN_Test\Test_DQN\Data\Process_canada_data\P13_days_sequences.h5"
#     reshaped_h5 = "D:\Rainbow_DQN_Test\Test_DQN\Data\Process_canada_data\P13_5_sec_sequences.h5"
#     dataset_name = "data"

#     # Create reshaper instance and reshape data into 5-seconds segments
#     reshaper = SequenceReshaper(sample_rate=64)
#     data = reshaper.read_h5(original_h5, dataset_name)
#     reshaped_data = reshaper.reshape(data, segment_duration=5)
#     print("Original shape:", data.shape)
#     print("Reshaped shape:", reshaped_data.shape)
#     print(f'the first sequence is: {reshaped_data[0]}')
#     key = input('Do you want to save data?: (y/n)')
#     if key=='y':
#         reshaper.save_h5(reshaped_h5, dataset_name, reshaped_data)
#         print('Done saving!')
#     else:
#         print('It is not saved!')
