from astropy.io import fits
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
from photutils.detection import DAOStarFinder
from astropy.stats import sigma_clipped_stats
from scipy.ndimage import median_filter

# Open and read the FITS file
fits_file = './examples/test_M31_linear.fits'
hdul = fits.open(fits_file)

# Display information about the file
hdul.info()

# Access the data from the primary HDU
data = hdul[0].data

# Access header information
header = hdul[0].header

# Prepare grayscale image only for star detection
is_color = False
if data.ndim == 3: 
    if data.shape[0] == 3:
        data = np.transpose(data, (1, 2, 0))
    is_color = True

if is_color:
    gray = np.mean(data, axis=2)
else:
    gray = data.copy()

# DAOStarFinder
mean, median, std = sigma_clipped_stats(gray, sigma=3.0)

# Detect stars
daofind = DAOStarFinder(fwhm=3.0, threshold=5.*std)
sources = daofind(gray - median)

# Create empty mask
mask = np.zeros_like(gray, dtype=np.uint8)

# Fill stars in the mask
if sources is not None:
    for star in sources:
        x, y = int(star['xcentroid']), int(star['ycentroid'])
        cv.circle(mask, (x, y), radius=10, color=255, thickness=-1)

# Save the mask and original
plt.imsave('./results/mask.png', mask, cmap='gray')
plt.imsave('./results/original.png', gray, cmap='gray')

# Convert to uint8 for OpenCV
image = ((data - data.min()) / (data.max() - data.min()) * 255).astype('uint8')

# Median filter
if is_color:
    I_erode = np.zeros_like(data, dtype=np.float32)
    for c in range(3):
        I_erode[:, :, c] = median_filter(data[:, :, c], size=5)
else:
    I_erode = median_filter(gray, size=5).astype(np.float32)

# Convert mask to float [0,1]
M = mask.astype(np.float32) / 255.0

# Gaussian blur to soften edges
M = cv.GaussianBlur(M, (11, 11), sigmaX=3)

# Convert original and eroded images to float
I_original = gray.astype(np.float32)
I_erode = I_erode.astype(np.float32)

# Interpolation
if is_color:
    I_final = np.zeros_like(data, dtype=np.float32)
    for c in range(3):
        I_final[:, :, c] = M * I_erode[:, :, c] + (1.0 - M) * data[:, :, c]
else:
    I_final = M * I_erode + (1.0 - M) * I_original

# Normalize final image
I_final_normalized = ((I_final - I_final.min()) / (I_final.max() - I_final.min()) * 255).astype(np.uint8)

# Save results
if is_color:
    plt.imsave('./results/original.png', (data - data.min()) / (data.max() - data.min()))
    plt.imsave('./results/final.png', I_final_normalized)
else:
    plt.imsave('./results/original.png', I_original, cmap='gray')
    plt.imsave('./results/final.png', I_final_normalized, cmap='gray')

# Close the file
hdul.close()
