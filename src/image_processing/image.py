from pathlib import Path

import cv2
import numpy
import numpy as np
from pdf2image import convert_from_path


# todo test on .pdf
def load(path: Path = None):
    """
    Load image from the template path or the image. Fill in all the parameters of Template class.
    """
    if path is None or not path.is_file():
        print("path is not a directory of a file")
        exit(1)

    if path.suffix.endswith('.pdf'):
        images = convert_from_path(path)
        if len(images) != 1:
            raise FileExistsError("pdf file " + path.as_posix() + "has several pages. 1 PDF page is "
                                                                  "required.")
        img = images[0]
    elif path.suffix.endswith('.jpg') or path.suffix.endswith('.png'):
        img = cv2.imread(path.as_posix())
    else:
        raise FileNotFoundError("Unsupported file type for reference file")

    return img


def good_matches(matches):
    """ Returns all the good matches according to Lowe's ratio test as a list.
    """
    # Find good matches using Lowe's ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)
    return good


def flann_matches(descr_img, descr_ref):
    """ Matches the key points of SIFT-features based on the given descriptors
    using a FLANN-based matcher, and returns the matches.

    """
    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    # Finding all matching key points
    return flann.knnMatch(descr_img, descr_ref, k=2)


class Image:
    # Initialising a SIFT-detector
    __detector = cv2.SIFT.create()

    _color: np.array
    _grey: np.array
    _inverse: np.array

    def __init__(self, image):
        if image is None or type(image) is not numpy.ndarray:
            raise ValueError("Image in none or wrong type.")
        self.__check_colors__(image)
        self.kpts_ref, self.descr_ref = self.__detector.detectAndCompute(self._color, None)

    def __check_colors__(self, image):
        if len(image.shape) == 3:
            self._set_color(image)
        elif len(image.shape) == 2:
            self._set_grey(image)
        else:
            raise FileNotFoundError("Unsupported file type - image has wrong number of channels")

    def _set_color(self, img):
        self._color = img
        self._grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self._set_inverse()

    def _set_grey(self, img):
        self._grey = img
        self._color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        self._set_inverse()

    def get_grey(self):
        return self._grey

    def get_color(self):
        return self._color

    def _set_inverse(self):
        self._inverse = cv2.bitwise_not(self._grey)

    def map_img_to_ref(self, image, method=cv2.RANSAC, ransac_thresh=5.0, min_match_count=100):
        """ Calculates features of the given image and reference image, matches
            them, finds the corresponding transformation from the reference image to
            the image (if enough good matches (specified by 'MIN_MATCH_COUNT') are
            found, and transforms the image to the reference image, which is then
            returned.
        """
        kpts_img, descr_img = self.__detector.detectAndCompute(image, None)

        # Matching of both images
        matches = flann_matches(descr_img, self.descr_ref)
        good = good_matches(matches)
        if not len(good) > min_match_count:
            print(f'Could not find enough good matches to match the images!')
            exit(-1)

        # Creating a numpy array from the key points which are good matches for
        # the image and the reference image, respectively
        img_pts = np.float32([kpts_img[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        ref_pts = np.float32([self.kpts_ref[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        # Computing the transformation from the reference image to the image
        transform_mat = cv2.findHomography(img_pts, ref_pts, method, ransac_thresh)[0]

        # Specifying the size of the resulting transformed-LHI image
        # Here: using size the of the reference image
        ref_cols, ref_rows = self._grey.shape
        dsize = (ref_rows, ref_cols)
        # Using the inverse transformation (image -> reference image)
        transformed = cv2.warpPerspective(image, transform_mat, dsize)
        return transformed

    def crop_image(self, pt1, pt2, eps: int):
        return self._color[pt1.x - eps:pt1.y - eps, pt2.x + eps:pt2.y + eps]

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

    def erode(self):
        # Creating kernel
        kernel = np.ones((2, 2), np.uint8)

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

    def render(self, directory: str, grey: bool):
        if grey:
            cv2.imwrite(directory, self._grey)
        else:
            cv2.imwrite(directory, self._color)
