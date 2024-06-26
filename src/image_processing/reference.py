
import cv2
import numpy as np

from image_processing.image import Image


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


class Reference(Image):

    # Initialising a SIFT-detector
    __detector = cv2.SIFT.create()

    def __init__(self, image: np.array):
        super().__init__(image)
        self.kpts_ref, self.descr_ref = self.__detector.detectAndCompute(self._color, None)

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
