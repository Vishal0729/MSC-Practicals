import imageio.v2 as imageio
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
# Input Agreement ============================================
sInputFileName = r"D:/MSC Practicals/Data Science/Practical - 1/Inputs/Angus.jpg"   # 
if not os.path.exists(sInputFileName):
    raise FileNotFoundError(f"Image not found at: {sInputFileName}")
InputData = imageio.imread(sInputFileName)
print('Input Data Values ===================================')
print('X: ', InputData.shape[0])
print('Y: ', InputData.shape[1])
print('Channels (RGB or RGBA): ', InputData.shape[2])
print('=====================================================')
# Processing Rules ===========================================
ProcessRawData = InputData.flatten()
y = InputData.shape[2] + 2
x = int(ProcessRawData.shape[0] / y)
ProcessData = pd.DataFrame(np.reshape(ProcessRawData, (x, y)))
sColumns = ['XAxis', 'YAxis', 'Red', 'Green', 'Blue']
if InputData.shape[2] == 4:   # if image has Alpha channel
    sColumns.append('Alpha')
ProcessData.columns = sColumns
ProcessData.index.names = ['ID']
print('Rows: ', ProcessData.shape[0])
print('Columns :', ProcessData.shape[1])
print('=====================================================')
plt.imshow(InputData)
plt.axis("off")
plt.show()
# Output Agreement ===========================================
OutputData = ProcessData
print('Storing File')
# Ensure folder exists
out_dir = r"D:/MSC Practicals/Data Science/Practical - 1/Outputs/"
os.makedirs(out_dir, exist_ok=True)
sOutputFileName = os.path.join(out_dir, "HORUS-Picture.csv")
OutputData.to_csv(sOutputFileName, index=False)
print('=====================================================')
print('Picture to HORUS - Done')
print('=====================================================')

