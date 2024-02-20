from reference_image import Image

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


def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


def pixel_val(pix, r1, s1, r2, s2):
    if 0 <= pix <= r1:
        return int(s1 / r1) * pix
    elif r1 < pix <= r2:
        return int((s2 - s1) / (r2 - r1)) * (pix - r1) + s1
    else:
        return int((255 - s2) / (255 - r2)) * (pix - r2) + s2


def extract_template(reference: Image, transformed_images, results_dir: Path = None, debug: bool = False):
    if transformed_images is None or len(transformed_images) == 0:
        print("empty directory of images\n")
        exit(1)
    if results_dir is None and debug is True:
        print("result dir cannot be None with debug mode on\n")
        exit(1)

    transformed_images.append(reference.image_grey)

    average = calculate_average_img(transformed_images)
    subt_image = cv2.bitwise_not(average)
    thresh, bw_mean_thresh = cv2.threshold(subt_image, 60, 255, cv2.THRESH_TOZERO)
    bw_mean_thresh_filter = 255 - bw_mean_thresh
    cv2.filterSpeckles(bw_mean_thresh_filter, 255, 10, 2000)

    if debug:
        # todo finish for some templates it might be essential
        subt = calculate_subtracted_img(transformed_images)
        subt_dir = results_dir / "subtr.png"
        cv2.imwrite(subt_dir.as_posix(), subt)

        average_dir = results_dir / "average.png"
        cv2.imwrite(average_dir.as_posix(), average)

        mean_speckles_dir = results_dir / "bw_mean_thresh_speckles.png"
        cv2.imwrite(mean_speckles_dir.as_posix(), bw_mean_thresh_filter)

    template_clean = adjust_gamma(bw_mean_thresh_filter, 2)
    return template_clean
