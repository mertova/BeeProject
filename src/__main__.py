import glob

import numpy as np

import lineUtils as lUtils
import pointUtils as pUtils
import line_recognition as lr
from cv2 import cv2
import template_extraction_utils as te
from sift_transformator import map_img_to_ref

documents_dir = '../data/scans/png/Niedersach-examples/'
transformed_dir = '../data/results/transformedQuality/'
ref_img_path = '../data/templates/Niedersach-empty-template.png'
results_template_path = '../data/results/extracting_template_out/'
results_lines_path = '../data/results/line_recognition_results/'
results_path = '../data/results/'


def main():
    images = load_grayscale_data(transformed_dir + "*.png")
    ref_image = cv2.imread(ref_img_path)

    cv2.imwrite(results_path + "results3/canny_grayscale.png", lr.sum_canny(images))

    sum_canny, max_val = lr.sum_canny(images)

    te.binary_thresholding(sum_canny, max_val)

    gray_transformed = []
    for img in images:
        gray_transformed.append(map_img_to_ref(img, ref_image, MIN_MATCH_COUNT=10))
    print("transformed all images")


def line_scanner_hough():
    template = cv2.imread(results_template_path + 'extracted_template.png')
    img = lr.preprocessing(cv2.cvtColor(template, cv2.COLOR_BGR2GRAY))
    cv2.imwrite(results_path+"results7/preprocessing_template.png", img)

    empty = np.copy(template)*0
    h_lines = lr.detect_lines_hough(img)
    line_image = lUtils.write_lines(empty, h_lines)
    cv2.imwrite(results_path + "results7/line_image_template_hough.png", line_image)

    # extended_lines = lr.make_lines_infinite(h_lines, template.shape[0], template.shape[1])
    # line_image = lUtils.write_lines(template, extended_lines)
    # cv2.imwrite(results_path + "results7/line_image_template_extended.png", line_image)

    intersections = lUtils.calculate_intersections(h_lines)
    point_image = pUtils.write_points(line_image, intersections, (255, 255, 0))
    x_centers, y_centers = pUtils.kmeans_xy(intersections)
    point_image = pUtils.write_points(point_image, x_centers, (0, 0, 255))
    point_image = pUtils.write_points(point_image, y_centers, (0, 0, 255))
    cv2.imwrite(results_path + "results7/point_image_template.png", point_image)


def template_postprocessing():
    template = cv2.imread(results_template_path + 'extracted_template.png', cv2.IMREAD_GRAYSCALE)
    contours = te.isolated_pix_remove(template)
    cv2.imwrite(results_path + "results5/pix_removal3.png", contours)


# Does not work for my purpose
# Todo check later
def line_scanner_cv2():
    template = cv2.imread(results_template_path + 'extracted_template.png')
    img = lr.fit_line_cv2(template)
    cv2.imwrite(results_path + "results4/extracted_lines_cv.png", img)


def load_grayscale_data(path):
    images = glob.glob(path)
    image_data = []
    for img in images:
        image_data.append(
            cv2.cvtColor(
                cv2.imread(img, 1), cv2.COLOR_BGR2GRAY)
        )
    return image_data


def write_data(images, path):
    for img in images:
        cv2.imwrite(path, img)


if __name__ == '__main__':
    line_scanner_hough()
