#!/usr/bin/env python3

# import sys
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
from scipy.ndimage import gaussian_filter
import warnings

# warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
# warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)
warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")

class get_watermark():
    def __init__(self):
        pass
    def normalize(self,x):
        _min = np.min(x)
        _max = np.max(x)
        return (x - _min) / (_max - _min)
    def get_watermarks(self,image_path:str)->str:
        """
        get watermark from image
        """
        buff = []
        for p in Path(image_path).glob("output_*.png"):
            buff.append(imageio.imread(p))
        images = np.array(buff)

        # Compute the gradients
        dx = np.gradient(images, axis=1).mean(axis=3)
        dy = np.gradient(images, axis=2).mean(axis=3)
        mean_dx = np.abs(np.mean(dx, axis=0))
        mean_dy = np.abs(np.mean(dy, axis=0))

        # Filter at a hand picked threshold
        threshold = 10
        salient = ((mean_dx > threshold) | (mean_dy > threshold)).astype(float)
        salient = self.normalize(gaussian_filter(salient, sigma=3))
        mask = ((salient > 0.2) * 255).astype(np.uint8)

        # Saved the computed mask
        imageio.imsave(image_path + "/mask.png", mask)
        return image_path + "/mask.png"
