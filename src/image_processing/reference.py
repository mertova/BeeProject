
import cv2
import numpy as np

from image_processing.image import Image


class Reference(Image):

    def __init__(self, image: np.array):
        super().__init__(image)

    def pen_elimination(self):
        """
        pen elimination frm the reference image
        H: 0-179, S: 0-255, V: 0-255
        """
        hsv = cv2.cvtColor(self._color, cv2.COLOR_BGR2HSV)

        # define range of blue color in HSV
        lower_blue = np.array([85, 0, 50], np.uint8)
        upper_blue = np.array([150, 255, 255], np.uint8)

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Bitwise-AND mask and original image
        mask_inverse = cv2.bitwise_not(mask)
        mask_inverse = cv2.filterSpeckles(mask_inverse, 255, 20, 200)
        res = cv2.bitwise_and(self._color, self._color, mask=mask_inverse[0])
        self._set_color(res + 255)

    def clean_averaged_form(self):
        cv2.imshow('orig', self._color)

        self.sharpening()
        self.erode()
        self.add_contrast()
        self.threshold2()
        self.sharpening()
        self.filter_speckles()
        cv2.imshow('image', self._color)
        cv2.waitKey(0)
        """
        self.add_contrast()
        self.sharpening()
        self.erode()

        self.threshold()
        self.filter_speckles()
        self.sharpening()
        """

