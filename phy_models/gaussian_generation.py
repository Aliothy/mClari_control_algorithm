import numpy as np
import cv2

# Parameters for the Gaussian function
mean = 0.0        # Mean of the Gaussian distribution
std_dev = 1     # Standard deviation of the distribution

# Create grid
nrows, ncols = 200, 200  # Resolution of the grid

# Calculate the height field using the Gaussian noise function
noise = np.random.normal(mean, std_dev, size=(nrows, ncols))

noise_flat = noise.flatten()
n_max = max(noise_flat)
n_min = min(noise_flat)
n_dist = n_max-n_min
noise = np.uint8(255*(noise/n_dist-n_min))
kernel = np.ones((3,3),np.float32)/9
filtered_image = cv2.filter2D(noise,-1,kernel)
# Print or write the data to be used in the MuJoCo XML
filename_filt = "gaussian_noise_filt.png"
cv2.imwrite(filename_filt,filtered_image)
filename = "gaussian_noise.png"
cv2.imwrite(filename,noise)