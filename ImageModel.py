import numpy as np
import cv2 as cv
from astropy.io import fits
from typing import Optional
from photutils.detection import DAOStarFinder

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