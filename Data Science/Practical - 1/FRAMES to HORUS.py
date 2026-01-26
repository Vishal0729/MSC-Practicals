import imageio.v2 as imageio  # Use v2 explicitly to avoid warnings
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Input Agreement ============================================
sDataBaseDir = 'D:/MSC Practicals/Data Science/Practical - 1/Outputs/temp'
f = 0

all_frames = []  # To collect data frames

for file in os.listdir(sDataBaseDir):
    if file.endswith(".jpg"):
        f += 1
        sInputFileName = os.path.join(sDataBaseDir, file)
        print('Process : ', sInputFileName)
        InputData = imageio.imread(sInputFileName)
        print('Input Data Values ===================================')
        print('X: ', InputData.shape[0])
        print('Y: ', InputData.shape[1])
        print('RGBA: ', InputData.shape[2])
        print('=====================================================')

        # Processing Rules ===========================================
        ProcessRawData = InputData.flatten()
        y = InputData.shape[2] + 2
        x = int(ProcessRawData.shape[0] / y)
        ProcessFrameData = pd.DataFrame(np.reshape(ProcessRawData, (x, y)))
        ProcessFrameData['Frame'] = file
        print('=====================================================')
        print('Process Data Values =================================')
        print('=====================================================')
        plt.imshow(InputData)
        plt.show()

        all_frames.append(ProcessFrameData)  # Append frame to the list

if f > 0:
    ProcessData = pd.concat(all_frames, ignore_index=True)  # Use pd.concat to combine data frames
    sColumns = ['XAxis', 'YAxis', 'Red', 'Green', 'Blue', 'FrameName']
    ProcessData.columns = sColumns
    ProcessData.index.names = ['ID']
    print('Rows: ', ProcessData.shape[0])
    print('Columns :', ProcessData.shape[1])
    print('=====================================================')
    # Output Agreement ===========================================
    OutputData = ProcessData
    print('Storing File')
    sOutputFileName = 'D:/MSC Practicals/Data Science/Practical - 1/Outputs/HORUS-Movie-Frame.csv'
    OutputData.to_csv(sOutputFileName, index=False)
    print('=====================================================')
    print('Processed : ', f, ' frames')
    print('=====================================================')
    print('Movie to HORUS - Done')
    print('=====================================================')

