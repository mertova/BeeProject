import glob
import line_recognition as lr
from cv2 import cv2
import template_extraction_utils as te
from sift_transformator import map_img_to_ref

documents_dir = '../data/scans/png/Sample-JKI-BS/'
transformed_dir = '../data/results/transformedQuality/'
ref_img_path = '../data/templates/Niedersach-empty-template.png'
results_template_path = '../data/results/extracting_template_out/'
results_lines_path = '../data/results/line_recognition_results/'


# missing classification and transformation
def main():
    images = load_data(documents_dir + "*.png")
    ref_image = cv2.imread(ref_img_path)

    gray_transformed = []
    for img in images:
        transformed = map_img_to_ref(img, ref_image, MIN_MATCH_COUNT=10)
        gray_transformed.append(cv2.cvtColor(transformed, cv2.COLOR_BGR2GRAY))
    print("transformed all images")
    # write transformed
    # write_data(gray_transformed, transformed_dir)

    # extract template from set of transformed scans
    template = te.extract_template(gray_transformed)
    cv2.imwrite(results_template_path + "extracted_template1.png", template)

    # Draw the lines on the  image
    lines = lr.detect_lines_hough(template)
    line_image = lr.write_lines(template, lines)
    cv2.imwrite(results_lines_path + "detected_lines1.png", line_image)
    lines_edges = cv2.addWeighted(template, 0.8, line_image, 1, 0)
    #cv2.imshow("lines ", lines_edges)

    print("bye bye, ciao, dovidenia, nashledanou, ")


def load_data(path):
    images = glob.glob(path)
    image_data = []
    for img in images:
        image_data.append(cv2.imread(img, 1))
    return image_data


def write_data(images, path):
    for img in images:
        cv2.imwrite(path, img)


if __name__ == '__main__':
    main()
