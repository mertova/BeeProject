import cv2
import numpy as np
import glob
import sift_transformator as st

results_dir = '../data/results/extracting_template_out/results3/'
example_blue = cv2.imread("../data/scans/png/Niedersach_examples_50/03_LHI_observation_reports_2000"
                          "-23_03_LHI_observation_reports_2000-23-1.png")
documents_dir = '../data/scans/png/Niedersach_examples_50/'
template = cv2.imread('../data/templates/template.png')
transformed_dir = '../data/results/transformed1/'
example_file = cv2.imread('../data/scans/png/Niedersach_examples_50/'
                          '03_LHI_observation_reports_2000-47_03_LHI_observation_reports_2000-47-1.png')


def load_data(path):
    images = glob.glob(path)
    image_data = []
    for pic in images:
        image_data.append(cv2.imread(pic, cv2.IMREAD_GRAYSCALE))
    return image_data


# H: 0-179, S: 0-255, V: 0-255
def extract_template_pen_elimination(img):
    cv2.imwrite(results_dir + "frame.png", img)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([85, 0, 50], np.uint8)
    upper_blue = np.array([150, 255, 255], np.uint8)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    mask_inverse = cv2.bitwise_not(mask)
    cv2.imwrite(results_dir + "mask_inverse.png", mask_inverse)
    cv2.filterSpeckles(mask_inverse, 255, 50, 2000)

    mask_speckless = cv2.bitwise_not(mask_inverse)
    cv2.imwrite(results_dir + "speckless_img.png", mask_speckless)

    grey_template = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.bitwise_and(grey_template, grey_template, mask=mask_inverse)
    cv2.imwrite(results_dir + "res0.png", res)
    res = res + mask_speckless
    cv2.filterSpeckles(res, 255, 1000, 2000)
    cv2.imwrite(results_dir + "res.png", res)

    return res


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
            avg_image = cv2.addWeighted(image_data[i], alpha, avg_image, beta, 0.0)
    return avg_image


def extract_template_averaging(images):
    if images is None or len(images) == 0:
        print("empty directory of images")
        return

    average = calculate_average_img(images)
    cv2.imwrite(results_dir + "average.png", average)
    gamma_correction(average, 5)


def gamma_correction(img, pixel_val):
    # Define parameters.
    r1 = 100
    s1 = 0
    r2 = 210
    s2 = 255

    # Vectorize the function to apply it to each value in the Numpy array.
    pixel_val_vec = np.vectorize(pixel_val)

    # Apply contrast stretching.
    contrast_stretched = pixel_val_vec(img, r1, s1, r2, s2)

    # Save edited image.
    cv2.imwrite(results_dir + 'contrast_stretch.png', contrast_stretched)


if __name__ == '__main__':
    # extract_template_pen_elimination(example_blue)
    template_grey = cv2.cvtColor(example_file, cv2.COLOR_BGR2GRAY)
    st.transform_dataset_grey(load_data(documents_dir + "*.png"), template_grey)
    transformed_images = load_data(transformed_dir + "*.png")
    extract_template_averaging(transformed_images)
