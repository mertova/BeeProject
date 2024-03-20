import cv2
import numpy as np


def pen_elimination(reference):
    """
    pen elimination frm the reference image
    H: 0-179, S: 0-255, V: 0-255
    """
    hsv = cv2.cvtColor(reference, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([85, 0, 50], np.uint8)
    upper_blue = np.array([150, 255, 255], np.uint8)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    mask_inverse = cv2.bitwise_not(mask)
    cv2.filterSpeckles(mask_inverse, 255, 20, 200)

    res = cv2.bitwise_and(reference, reference, mask=mask_inverse)
    return res + 255


def calculate_average(pen_free_img, data_sample):
    """
    calculate average from the input data samples
    :return: average image
    """
    avg_image = cv2.cvtColor(pen_free_img, cv2.COLOR_BGR2GRAY)
    for i in range(len(data_sample)):
        if i == 0:
            pass
        else:
            alpha = 1.0 / (i + 1)
            beta = 1.0 - alpha
            avg_image = cv2.addWeighted(data_sample[i], alpha, avg_image, beta, 1.0)
    return avg_image


def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)
