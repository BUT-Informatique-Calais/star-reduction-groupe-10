from PyQt6.QtCore import QThread, pyqtSignal
import numpy as np
import cv2 as cv
from scipy.ndimage import median_filter
from photutils.detection import DAOStarFinder
from astropy.stats import sigma_clipped_stats
from API_astrometry import upload_image_API

class StarReductionThread(QThread):
    finished = pyqtSignal(np.ndarray)

    def __init__(self, model, use_api=False, file_path=None):
        super().__init__()
        self.model = model
        self.use_api = use_api
        self.file_path = file_path
        
        self.mask_radius = model.mask_radius
        self.median_size = model.median_size
        self.gaussian_kernel = model.gaussian_kernel

    def run(self):
        """Traitement lourd dans un thread séparé"""
        gray = self.model.gray
        data = self.model.data
        is_color = self.model.is_color

        # Mask
        if self.use_api:
            mask = upload_image_API(self.file_path)
            if mask is None:
                self.finished.emit(self.model.image_orig)
                return
        
        else:       
            if self.model.stars is None:
                # DAOStarFinder
                mean, median, std = sigma_clipped_stats(gray, sigma=3.0)
                
                # Detect stars
                daofind = DAOStarFinder(fwhm=3.0, threshold=5.0 * std)
                self.model.stars = daofind(gray - median)

            # Create empty mask
            mask = np.zeros_like(gray, dtype=np.uint8)
            
            # Fill stars in the mask
            if self.model.stars is not None:
                for star in self.model.stars:
                    x, y = int(star['xcentroid']), int(star['ycentroid'])
                    cv.circle(mask, (x, y), self.mask_radius, color=255, thickness=-1)

        # Median
        if self.median_size % 2 == 0:
            self.median_size += 1

        # Median filter
        if is_color:
            I_erode = np.zeros_like(data, dtype=np.float32)
            for c in range(3):
                I_erode[:, :, c] = median_filter(data[:, :, c], size=self.median_size)
        else:
            I_erode = median_filter(gray, size=self.median_size).astype(np.float32)

        # Convert mask to float [0,1]
        M = mask.astype(np.float32) / 255.0
        
        # Gaussian blur to soften edges
        M = cv.GaussianBlur(M, (self.gaussian_kernel, self.gaussian_kernel), sigmaX=3)
        
        # Interpolation
        if is_color:
            I_final = np.zeros_like(data, dtype=np.float32)
            for c in range(3):
                I_final[:, :, c] = M * I_erode[:, :, c] + (1.0 - M) * data[:, :, c]
        else:
            I_final = M * I_erode + (1.0 - M) * gray
            
        # Convert RGB -> BGR
        I_final = cv.cvtColor(I_final, cv.COLOR_RGB2BGR)
        
        # Normalize final image
        I_final_normalized = self.model._normalize(I_final)
        self.model.I_final_normalized = I_final_normalized

        self.finished.emit(I_final_normalized)
