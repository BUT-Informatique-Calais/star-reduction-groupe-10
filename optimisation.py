from PyQt6.QtCore import QThread, pyqtSignal
import numpy as np
import cv2 as cv
from scipy.ndimage import median_filter
from photutils.detection import DAOStarFinder
from astropy.stats import sigma_clipped_stats

class StarReductionThread(QThread):
    finished = pyqtSignal(np.ndarray)  # signal pour renvoyer le résultat

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.mask_radius = model.mask_radius
        self.median_size = model.median_size
        self.gaussian_kernel = model.gaussian_kernel

    def run(self):
        """Traitement lourd dans un thread séparé"""
        gray = self.model.gray
        data = self.model.data
        is_color = self.model.is_color

        # Détecte les étoiles une seule fois
        if self.model.stars is None:
            mean, median, std = sigma_clipped_stats(gray, sigma=3.0)
            daofind = DAOStarFinder(fwhm=3.0, threshold=5.0 * std)
            self.model.stars = daofind(gray - median)

        # Création du masque
        mask = np.zeros_like(gray, dtype=np.uint8)
        if self.model.stars is not None:
            for star in self.model.stars:
                x, y = int(star['xcentroid']), int(star['ycentroid'])
                cv.circle(mask, (x, y), self.mask_radius, color=255, thickness=-1)

        # Filtre médian
        if self.median_size % 2 == 0:
            self.median_size += 1

        if is_color:
            I_erode = np.zeros_like(data, dtype=np.float32)
            for c in range(3):
                I_erode[:, :, c] = median_filter(data[:, :, c], size=self.median_size)
        else:
            I_erode = median_filter(gray, size=self.median_size).astype(np.float32)

        # Masque float + Gaussian blur
        M = mask.astype(np.float32) / 255.0
        M = cv.GaussianBlur(M, (self.gaussian_kernel, self.gaussian_kernel), sigmaX=3)

        # Interpolation
        if is_color:
            I_final = np.zeros_like(data, dtype=np.float32)
            for c in range(3):
                I_final[:, :, c] = M * I_erode[:, :, c] + (1.0 - M) * data[:, :, c]
        else:
            I_final = M * I_erode + (1.0 - M) * gray
        I_final = cv.cvtColor(I_final, cv.COLOR_RGB2BGR)
        
        I_final_normalized = self.model._normalize(I_final)
        self.model.I_final_normalized = I_final_normalized

        self.finished.emit(I_final_normalized)
