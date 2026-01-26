#pip install opencv-python
import os
import shutil
import cv2
# Input Agreement ============================================
sInputFileName = 'D:/MSC Practicals/Data Science/Practical - 1/Inputs/dog.mp4'
sDataBaseDir = 'D:/MSC Practicals/Data Science/Practical - 1/Outputs/temp'
if os.path.exists(sDataBaseDir):
    shutil.rmtree(sDataBaseDir)
if not os.path.exists(sDataBaseDir):
    os.makedirs(sDataBaseDir)
print('=====================================================')
print('Start Movie to Frames')
print('=====================================================')
vidcap = cv2.VideoCapture(sInputFileName)
success, image = vidcap.read()
count = 0
while success:
    sFrame = os.path.join(sDataBaseDir, 'dog-frame-{:04d}.jpg'.format(count))
    print('Extracted: ', sFrame)
    cv2.imwrite(sFrame, image)
    success, image = vidcap.read()
    if os.path.exists(sFrame) and os.path.getsize(sFrame) == 0:
        os.remove(sFrame)
        print('Removed: ', sFrame)
        count -= 1
    if cv2.waitKey(10) == 27: 
        break   
    count += 1
print('=====================================================')
print('Generated: ', count, ' Frames')
print('=====================================================')
print('Movie to Frames HORUS - Done')
print('=====================================================')

