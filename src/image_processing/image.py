import cv2
import numpy
import numpy as np

from vertex import Vertex


class Image:

    _color: np.array
    _grey: np.array
    _inverse: np.array

    def __init__(self, image):
        if image is None or type(image) is not numpy.ndarray:
            raise ValueError("Image is None or wrong type.")
        self.__set_image(image)

    def __set_image(self, image):
        """
        Evaluates channels (shape) of numpy array and sets color, grey and inverse images.
        :param image: input numpy array
        :raise ValueError when image is wrong shape.
        """
        if len(image.shape) == 3:
            self._set_color(image)
        elif len(image.shape) == 2:
            self._set_grey(image)
        else:
            raise ValueError("Unsupported file type - image has wrong number of channels")

    def _set_color(self, img):
        self._color = img
        self._grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self._inverse = cv2.bitwise_not(self._grey)

    def _set_grey(self, img):
        self._grey = img
        self._color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        self._inverse = cv2.bitwise_not(self._grey)

    def get_grey(self):
        return self._grey

    def get_color(self):
        return self._color

    def get_inverse(self):
        return self._inverse

    def preprocessing(self, form_inverse):
        text_scan_not = cv2.subtract(self.get_inverse(), form_inverse)
        text_scan = cv2.bitwise_not(text_scan_not)
        self._set_grey(text_scan)
        self.sharpening()

    def threshold(self):
        ret, thresh = cv2.threshold(self._inverse, 100, 255, cv2.THRESH_TOZERO)
        thresh_inverse = cv2.bitwise_not(thresh)
        self._set_grey(thresh_inverse)

    def median_blur(self):
        median = cv2.medianBlur(self._grey, 3)
        self._set_grey(median)

    def filter_speckles(self):
        clean = cv2.filterSpeckles(self._grey, 255, 10, 2000)
        self._set_grey(clean[0])

    def erode(self, n):
        # Creating kernel
        kernel = np.ones((n, n), np.uint8)

        # Using cv2.erode() method
        erode = cv2.erode(self._color, kernel, cv2.BORDER_REFLECT)
        self._set_color(erode)

    def add_contrast(self):
        # Adjust the brightness and contrast
        # g(i,j)=α⋅f(i,j)+β
        # control Contrast by 1.5
        alpha = 1.2
        # control brightness by 50
        beta = 1.
        image2 = cv2.convertScaleAbs(self._grey, alpha=alpha, beta=beta)
        self._set_grey(image2)

    def add_weighted(self, img):
        # add greyscale img to reference
        added = cv2.addWeighted(self.get_grey(), 0.8, img, 0.2, 0)
        # set reference image - color and inverse will be automatically calculated
        self._set_grey(added)

    def sharpening(self):
        # Create the sharpening kernel
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

        # Sharpen the image
        sharpened_image = cv2.filter2D(self._grey, -1, kernel)
        self._set_grey(sharpened_image)

    # thresholding
    def threshold2(self):
        thr = cv2.threshold(self._grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        self._set_grey(thr)

    # opening - erosion followed by dilation
    def opening(self):
        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(self._grey, cv2.MORPH_OPEN, kernel)
        self._set_grey(opening)

