import glob

import numpy as np

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


# missing classification and transformation
def main():
    images = load_grayscale_data(transformed_dir + "*.png")
    ref_image = cv2.imread(ref_img_path)

    #cv2.imwrite(results_path + "results3/canny_grayscale.png", lr.sum_canny(images))

    # sum_canny, max_val = lr.sum_canny(images)

    # te.binary_thresholding(sum_canny, max_val)


    '''
    gray_transformed = []
    for img in images:
        gray_transformed.append(map_img_to_ref(img, ref_image, MIN_MATCH_COUNT=10))
    print("transformed all images")
    # write transformed
    # write_data(gray_transformed, transformed_dir)
    '''
    # extract template from set of transformed scan
    #template = te.extract_template(ref_image)
    #cv2.imwrite(results_path + "results3/extracted_template1.png", template)

    print("bye bye, ciao, dovidenia, nashledanou, dovidzenia, mua mua ")


def line_scanner_hough():
    template = cv2.imread(results_template_path + 'extracted_template.png')
    img = lr.preprocessing(cv2.cvtColor(template, cv2.COLOR_BGR2GRAY))
    cv2.imwrite(results_path+"results7/preprocessing_template.png", img)

    h_lines = lr.detect_lines_hough(img)

    extended_lines = lr.make_lines_infinite(h_lines, template.shape[0], template.shape[1])
    line_image = lr.write_lines(template, extended_lines)
    cv2.imwrite(results_path + "results7/line_image_template_extended.png", line_image)

    reduced_lines = lr.reduce_lines(extended_lines)
    line_image = lr.write_lines(template, reduced_lines)
    cv2.imwrite(results_path + "results7/line_image_template_reduced.png", line_image)

    point_image = lr.write_points(line_image, lr.calculate_intersections(reduced_lines))
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
