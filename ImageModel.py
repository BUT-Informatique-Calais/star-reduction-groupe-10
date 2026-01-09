import numpy as np
import cv2 as cv
from astropy.io import fits
from typing import Optional
from photutils.detection import DAOStarFinder
from astropy.stats import sigma_clipped_stats
from scipy.ndimage import median_filter


class ImageModel:
    def __init__(self):
        self.data: Optional[np.ndarray] = None
        self.gray: Optional[np.ndarray] = None
        self.image_orig: Optional[np.ndarray] = None
        self.I_final_normalized: Optional[np.ndarray] = None

        self.is_color: bool = False

        self.stars = None

        # Processing parameters
        self.mask_radius: int = 10
        self.median_size: int = 5
        self.gaussian_kernel: int = 11

    def _normalize(self, img: np.ndarray) -> np.ndarray:
        """Normalize image to uint8 [0,255]"""
        vmin = img.min()
        vmax = img.max()
        if vmax == vmin:
            return np.zeros_like(img, dtype=np.uint8)
        return ((img - vmin) / (vmax - vmin) * 255).astype(np.uint8)

    def load_fits(self, file_path: str):
        """Load FITS file and prepare data"""
        # Open and read the FITS file
        hdul = fits.open(file_path)
        
        # Display information about the file
        hdul.info()
        
        # Access the data from the primary HDU
        self.data = hdul[0].data.astype(np.float32)

        # Prepare grayscale image only for star detection
        self.is_color = False
        if self.data.ndim == 3: 
            if self.data.shape[0] == 3:
                self.data = np.transpose(self.data, (1, 2, 0))
            self.is_color = True

        if self.is_color:
            self.gray = np.mean(self.data, axis=2)
        else:
            self.gray = self.data.copy()
        
        # Prepare image for display
        if self.is_color:
            self.image_orig = cv.cvtColor(self._normalize(self.data), cv.COLOR_RGB2BGR)
        else:
            self.image_orig = self._normalize(self.gray)

        self.I_final_normalized = self.image_orig.copy()
        
        # Close the file
        hdul.close()


    def apply_star_reduction(self) -> np.ndarray:
        """Apply star reduction using DAOStarFinder"""

        if self.median_size % 2 == 0:
            self.median_size += 1

        if self.stars is None:
            # DAOStarFinder
            mean, median, std = sigma_clipped_stats(self.gray, sigma=3.0)
            
            # Detect stars
            daofind = DAOStarFinder(fwhm=3.0, threshold=5.0 * std)
            self.stars = daofind(self.gray - median)

        # Create empty mask
        mask = np.zeros_like(self.gray, dtype=np.uint8)
        
        # Fill stars in the mask
        if self.stars is not None:
            for star in self.stars:
                x, y = int(star['xcentroid']), int(star['ycentroid'])
                cv.circle(mask, (x, y), self.mask_radius, color=255, thickness=-1)

        # Median filter
        if self.is_color:
            I_erode = np.zeros_like(self.data, dtype=np.float32)
            for c in range(3):
                I_erode[:, :, c] = median_filter(self.data[:, :, c], size=self.median_size)
        else:
            I_erode = median_filter(self.gray, size=self.median_size).astype(np.float32)

        # Convert mask to float [0,1]
        M = mask.astype(np.float32) / 255.0

        # Gaussian blur to soften edges
        M = cv.GaussianBlur(M, (self.gaussian_kernel, self.gaussian_kernel), sigmaX=3)

        # Convert original and eroded images to float
        I_original = self.gray.astype(np.float32)
        I_erode = I_erode.astype(np.float32)

        # Interpolation
        if self.is_color:
            I_final = np.zeros_like(self.data, dtype=np.float32)
            for c in range(3):
                I_final[:, :, c] = (
                    M * I_erode[:, :, c] + (1.0 - M) * self.data[:, :, c]
                )
        else:
            I_final = M * I_erode + (1.0 - M) * I_original

        # Convert RGB -> BGR
        I_final = cv.cvtColor(I_final, cv.COLOR_RGB2BGR)
    
        # Normalize final image
        self.I_final_normalized = self._normalize(I_final)

        return self.I_final_normalized
