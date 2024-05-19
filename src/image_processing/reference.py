
import cv2
import numpy as np

from image_processing.image import Image



def adjust_gamma(image, gamma=1.0):
    # build a lookup classes mapping the pixel values [0, 255] to
    # their adjusted gamma values
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup classes
    return cv2.LUT(image, table)


class Reference(Image):

    def __init__(self, image: np.array):
        if image is None:
            raise ValueError("Template path does not exist")

        super().__init__(image)

    def pen_elimination(self):
        """
        pen elimination frm the reference image
        H: 0-179, S: 0-255, V: 0-255
        """
        hsv = cv2.cvtColor(self.color, cv2.COLOR_BGR2HSV)

        # define range of blue color in HSV
        lower_blue = np.array([85, 0, 50], np.uint8)
        upper_blue = np.array([150, 255, 255], np.uint8)

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Bitwise-AND mask and original image
        mask_inverse = cv2.bitwise_not(mask)
        cv2.filterSpeckles(mask_inverse, 255, 20, 200)

        res = cv2.bitwise_and(self.color, self.color, mask=mask_inverse)
        self.color = res + 255

    def clean_image(self):
        original = self.grey
        self.set_inverse()
        thresh, bw_mean_thresh = cv2.threshold(self.inverse, 60, 255, cv2.THRESH_TOZERO)
        bw_mean_thresh_filter = 255 - bw_mean_thresh
        cv2.filterSpeckles(bw_mean_thresh_filter, 255, 10, 2000)
        self.color = adjust_gamma(bw_mean_thresh_filter, 2)
        return original, bw_mean_thresh_filter


