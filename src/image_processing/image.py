from pathlib import Path

import cv2
import numpy as np
from pdf2image import convert_from_path


# todo test on .pdf
def load(self, path: Path = None):
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
    detector = cv2.SIFT.create()

    color: np.array
    grey: np.array
    inverse: np.array

    def __init__(self, image):
        self.check_colors(image)
        self.kpts_ref, self.descr_ref = self.detector.detectAndCompute(self.color, None)

    def get_grey(self):
        return cv2.cvtColor(self.color, cv2.COLOR_BGR2GRAY)

    def set_inverse(self):
        self.inverse = cv2.bitwise_not(preprocessing.erode(self.grey))

    def map_img_to_ref(self, image, method=cv2.RANSAC, ransac_thresh=5.0, min_match_count=100):
        """ Calculates features of the given image and reference image, matches
            them, finds the corresponding transformation from the reference image to
            the image (if enough good matches (specified by 'MIN_MATCH_COUNT') are
            found, and transforms the image to the reference image, which is then
            returned.
        """
        kpts_img, descr_img = self.detector.detectAndCompute(image, None)

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
        ref_cols, ref_rows = self.grey.shape
        dsize = (ref_rows, ref_cols)
        # Using the inverse transformation (image -> reference image)
        transformed = cv2.warpPerspective(image, transform_mat, dsize)
        return transformed




    def check_colors(self, image):
        if len(image.shape) == 3:
            self.color = image
            self.grey = self.get_grey()
        elif len(image.shape) == 2:
            self.color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            self.grey = image
        else:
            raise FileNotFoundError("Unsupported file type - image has wrong number of channels")

    def crop_image(self, pt1, pt2, eps: int):
        return self.color[pt1.x - eps:pt1.y - eps, pt2.x + eps:pt2.y + eps]
