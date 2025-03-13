import cv2
import numpy as np

def read_image(filename: str):
    return cv2.imread(filename)


# Blur detection function
# Calculates how blurry a picture is
# Input: Image as an RGB pixel array
def blur_detection(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
    laplacian_array = laplacian.flatten()
    return np.var(laplacian_array)


# Green proportion function
# Calculates the green proportions of an image
# Input: Image as an RGB pixel array
def green_prop(image):
    if image.shape[-1] == 3:
        im_r, im_g, im_b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
        sum_r = np.sum(im_r.astype(np.float64))
        sum_g = np.sum(im_g.astype(np.float64))
        sum_b = np.sum(im_b.astype(np.float64))
        return sum_g / (sum_r + sum_g + sum_b)
    else:
        raise ValueError("Image must have three channels (RGB).")
