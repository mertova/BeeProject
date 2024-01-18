import cv2
import numpy as np
from pathlib import Path


def load_data_grey(path: Path):
    if path is None:
        print("Path is None")
        raise SystemExit(1)

    p = path.glob('**/*.png')
    files = [x for x in p if x.is_file()]
    image_data = []
    for file in files:
        image_data.append(cv2.imread(file.as_posix(), cv2.IMREAD_GRAYSCALE))
    return image_data


# H: 0-179, S: 0-255, V: 0-255
def pen_elimination(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([85, 0, 50], np.uint8)
    upper_blue = np.array([150, 255, 255], np.uint8)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    mask_inverse = cv2.bitwise_not(mask)
    cv2.filterSpeckles(mask_inverse, 255, 50, 2000)

    mask_speckles = cv2.bitwise_not(mask_inverse)

    grey_template = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.bitwise_and(grey_template, grey_template, mask=mask_inverse)
    res = res + mask_speckles
    cv2.filterSpeckles(res, 255, 1000, 2000)

    return res


def calculate_subtracted_img(image_data):
    subt_image = cv2.bitwise_not(image_data[0])
    for i in range(len(image_data)):
        if i == 0:
            pass
        else:
            subt_image = subt_image - cv2.bitwise_not(image_data[i])
    return subt_image


# calculate average from the input set of images
# returns image
def calculate_average_img(image_data):
    avg_image = image_data[0]
    for i in range(len(image_data)):
        if i == 0:
            pass
        else:
            alpha = 1.0 / (i + 1)
            beta = 1.0 - alpha
            avg_image = cv2.addWeighted(image_data[i], alpha, avg_image, beta, 1.0)
    return avg_image


def gamma_correction(img):
    # Define parameters.
    r1 = 150
    s1 = 0
    r2 = 200
    s2 = 255

    # Vectorize the function to apply it to each value in the Numpy array.
    pixel_val_vec = np.vectorize(pixel_val)

    # Apply contrast stretching.
    return pixel_val_vec(img, r1, s1, r2, s2)


def pixel_val(pix, r1, s1, r2, s2):
    if 0 <= pix <= r1:
        return (s1 / r1)*pix
    elif r1 < pix <= r2:
        return ((s2 - s1)/(r2 - r1)) * (pix - r1) + s1
    else:
        return ((255 - s2)/(255 - r2)) * (pix - r2) + s2
