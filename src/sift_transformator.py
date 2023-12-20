import numpy as np
import cv2

transformed_dir = '../data/results/transformed1/'


def flann_matches(descr_img, descr_ref):
    """ Matches the key points of SIFT-features based on the given descriptors
    using a FLANN-based matcher, and returns the matches.

    """
    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    # Finding all matching key points
    return flann.knnMatch(descr_img, descr_ref, k=2)


def good_matches(matches):
    """ Returns all the good matches according to Lowe's ratio test as a list.
    """
    # Find good matches using Lowe's ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)
    return good


def map_img_to_ref(image, ref_image, method=cv2.RANSAC, ransac_thresh=5.0, min_match_count=100):
    """ Calculates features of the given image and reference image, matches
        them, finds the corresponding transformation from the reference image to
        the image (if enough good matches (specified by 'MIN_MATCH_COUNT') are
        found, and transforms the image to the reference image, which is then
        returned.
    """
    # Initialising a SIFT-detector
    detector = cv2.SIFT.create()
    kpts_img, descr_img = detector.detectAndCompute(image, None)
    kpts_ref, descr_ref = detector.detectAndCompute(ref_image, None)

    # Matching of both images
    matches = flann_matches(descr_img, descr_ref)
    good = good_matches(matches)
    if not len(good) > min_match_count:
        print(f'Could not find enough good matches to match the images!')
        exit(-1)

    # Creating a numpy array from the key points which are good matches for
    # the image and the reference image, respectively
    img_pts = np.float32([kpts_img[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    ref_pts = np.float32([kpts_ref[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    # Computing the transformation from the reference image to the image
    transform_mat = cv2.findHomography(img_pts, ref_pts, method, ransac_thresh)[0]

    # Specifying the size of the resulting transformed image
    # Here: using size the of the reference image
    ref_cols, ref_rows = ref_image.shape
    dsize = (ref_rows, ref_cols)
    # Using the inverse transformation (image -> reference image)
    transformed = cv2.warpPerspective(image, transform_mat, dsize)
    return transformed


def transform_dataset_grey(images, template_grey):
    if images is None or len(images) == 0:
        print("empty directory of images")
        return
    gray_transformed = []
    i = 0
    for img in images:
        transformed = map_img_to_ref(img.copy(), template_grey)
        cv2.imwrite(transformed_dir + i.__str__() + ".png", transformed)
        gray_transformed.append(transformed)
        i += 1
    print("transformed all images")
