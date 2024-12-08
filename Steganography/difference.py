import numpy as np
import cv2
from math import log10, sqrt
from PIL import Image
from skimage.metrics import structural_similarity as ssim

class DifferenceStego:
    @staticmethod
    def calculatePSNR(original, compressed):
        mse = np.mean((original - compressed) ** 2)
        if mse == 0:  # MSE is zero means no noise is present in the signal
            return 100
        max_pixel = 255.0
        psnr = 20 * log10(max_pixel / sqrt(mse))
        return psnr

    @staticmethod
    def calculateMSE(imageA, imageB):
        # the 'Mean Squared Error' between the two images
        mse = np.mean((imageA - imageB) ** 2)
        return mse

    @staticmethod
    def calculateSSIM(imageA, imageB):
        # Convert the images to grayscale
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        
        # Compute the Structural Similarity Index (SSIM)
        (score, diff) = ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")
        return score
