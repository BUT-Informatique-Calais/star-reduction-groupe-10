from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from photutils.detection import DAOStarFinder
from astropy.stats import sigma_clipped_stats

# Open and read the FITS file
fits_file = './examples/test_M31_linear.fits'
hdul = fits.open(fits_file)

# Display information about the file
hdul.info()

# Access the data from the primary HDU
data = hdul[0].data

# Access header information
header = hdul[0].header

# Handle both monochrome and color images
if data.ndim == 3:
    # Color image - need to transpose to (height, width, channels)
    if data.shape[0] == 3:  # If channels are first: (3, height, width)
        data = np.mean(data, axis=0)
    else:
        data = np.mean(data, axis=2)

# DAOStarFinder
mean, median, std = sigma_clipped_stats(data, sigma=3.0)

# Detect stars
daofind = DAOStarFinder(fwhm=3.0, threshold=5.*std)
sources = daofind(data - median)

# Create empty mask
mask = np.zeros_like(data, dtype=np.uint8)

# Fill stars in the mask
if sources is not None:
    for star in sources:
        x, y = int(star['xcentroid']), int(star['ycentroid'])
        mask[y, x] = 255

# Save the mask
plt.imsave('./results/mask.png', mask, cmap='gray')

# Close the file
hdul.close()