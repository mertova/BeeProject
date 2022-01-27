""""""

import numpy as np
import cv2


def map_img_to_ref(image, ref_image, method=cv2.RANSAC, ransac_thresh=5.0,
                   MIN_MATCH_COUNT=1000):
    """ Calculates features of the given image and reference image, matches
        them, finds the corresponding transformation from the reference image to
        the image (if enough good matches (specified by 'MIN_MATCH_COUNT') are
        found, and transforms the image to the reference image, which is then
        returned.

    """
    # Initialising a SIFT-detector
    detector = cv2.SIFT_create()
    kpts_img, descr_img = detector.detectAndCompute(image, None)
    kpts_ref, descr_ref = detector.detectAndCompute(ref_image, None)

    # Matching of both images
    matches = flann_matches(descr_img, descr_ref)
    good = good_matches(matches)
    num_good_matches = len(good)
    if not num_good_matches > MIN_MATCH_COUNT:
        print(f'Could not find enough good matches to match the images!')
        exit(-1)

    # Creating a numpy array from the keypoints which are good matches for
    # the image and the reference image, respectively
    ref_pts = np.float32([kpts_ref[m.queryIdx].pt for m in
                          good]).reshape(-1, 1, 2)
    img_pts = np.float32([kpts_img[m.trainIdx].pt for m in
                          good]).reshape(-1, 1, 2)

    # Computing the transformation from the reference image to the image
    transform_mat, _ = cv2.findHomography(ref_pts, img_pts, method,
                                          ransac_thresh)
    print("transformacna matica: ", transform_mat)

    # Specifying the size of the resulting transformed image
    # Here: using size the of the reference image
    ref_cols, ref_rows, _ = ref_image.shape
    dsize = (ref_rows, ref_cols)
    # Using the inverse transformation (image -> reference image)
    transformed = cv2.warpPerspective(image, transform_mat, dsize,
                                      flags=cv2.WARP_INVERSE_MAP)
    return transformed


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
    """ Matches the keypoints of SIFT-features based on the given descriptors
    using a FLANN-based matcher, and returns the matches.

    """
    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    print(type(flann))
    # Finding all matching keypoints
    matches = flann.knnMatch(descr_ref, descr_img, k=2)
    print(matches[0][0].distance)
    return matches
