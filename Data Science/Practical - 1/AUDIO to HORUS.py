from scipy.io import wavfile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
def show_info(aname, a, r):
    print('----------------')
    print("Audio:", aname)
    print('----------------')
    print("Rate:", r)
    print('----------------')
    print("Shape:", a.shape)
    print("dtype:", a.dtype)
    print("min, max:", a.min(), a.max())
    print('----------------')
    plot_info(aname, a, r)
def plot_info(aname, a, r):
    plt.title(f"Signal Wave - {aname} at {r} Hz")
# Handle mono or multi-channel
    if a.ndim == 1:
        plt.plot(a, label="Ch1")
    else:
        for ch in range(a.shape[1]):
            plt.plot(a[:, ch], label=f"Ch{ch+1}")
    plt.legend(loc="upper right")
    plt.show()
def process_audio(path, expected_channels):
    print('=====================================================')
    print('Processing : ', path)
    print('=====================================================')
    rate, data = wavfile.read(path)
    show_info(f"{expected_channels} channel", data, rate)
# Convert to DataFrame safely
    if data.ndim == 1:
        df = pd.DataFrame(data, columns=['Ch1'])
    else:
        ch_count = data.shape[1]
        cols = [f"Ch{i+1}" for i in range(ch_count)]
        df = pd.DataFrame(data, columns=cols)
        # Define output directory
    output_dir = 'D:/MSC Practicals/Data Science/Practical - 1/Outputs/prac-1G/'
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get only the filename (e.g., "2ch-sound.wav")
    filename = os.path.basename(path)
    
    # Replace .wav with .csv (e.g., "2ch-sound.csv")
    csv_filename = filename.replace(".wav", ".csv")
    
    # Create full output path
    out = os.path.join(output_dir, csv_filename)
    
    df.to_csv(out, index=False)
    print(f"Saved: {out}")
    
# Process files
process_audio('D:/MSC Practicals/Data Science/Practical - 1/Inputs/prac-1G/2ch-sound.wav', 2)
process_audio('D:/MSC Practicals/Data Science/Practical - 1/Inputs/prac-1G/4ch-sound.wav', 4)
process_audio('D:/MSC Practicals/Data Science/Practical - 1/Inputs/prac-1G/6ch-sound.wav', 6)
process_audio('D:/MSC Practicals/Data Science/Practical - 1/Inputs/prac-1G/8ch-sound.wav', 8)
print('=====================================================')
print('Audio to HORUS - Done')
print('=====================================================')