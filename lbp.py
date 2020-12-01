import numpy as np
from skimage import feature
import cv2
import matplotlib.pyplot as plt

class LocalBinaryPatterns:
    def __init__(self, nPoints, radius_of_scanning):
        self.nPoints = nPoints
        self.radius_of_scanning = radius_of_scanning

    # def local_binary_pattern(self, IMG, nPoints, radius_of_scanning):

    
    def describe(self, image, RGB=False, eps=1e-7):
        if RGB==True:
            i = 3
        else:
            i=1
        for j in range(i):
            if RGB==True:
                IMG = image[:,:,j]
            else:
                IMG = image
            lbp = feature.local_binary_pattern(IMG, self.nPoints, self.radius_of_scanning)
            hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, 256, 1))

            # normalize the histogram
            hist = hist.astype("float")
            hist /= (hist.sum() + eps)
            if j == 0:
                Hist = hist
            else:
                Hist = np.concatenate((Hist, hist))
        # return the histogram of Local Binary Patterns
        return Hist



    def compute_LBP(self, img, RGB=False, plot=False, transform_image=False):
        LBP = None
        if RGB == False:
            method_name = "LBP"
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if transform_image:
                # "LBP" variable is not necessary for object detection. It only shows how LBP works
                LBP = feature.local_binary_pattern(gray_img, self.nPoints, self.radius_of_scanning, method="uniform")
            # only histogram is needed for object detection
            hist = self.describe(gray_img)

        else:
            method_name = "RGB-LBP"
            if transform_image:
                R = feature.local_binary_pattern(img[:, :, 0], 8, 2, method="uniform")
                G = feature.local_binary_pattern(img[:, :, 1], 8, 2, method="uniform")
                B = feature.local_binary_pattern(img[:, :, 2], 8, 2, method="uniform")
                LBP = np.vstack((R, G))
                LBP = np.vstack((LBP, B))
            # same
            hist = self.describe(img, RGB=True)

        # Show an image
        if plot:
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.show()

        return LBP, hist
