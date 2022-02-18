from cv2 import cv2
import statistics
import numpy
import numpy as np
from matplotlib import pyplot as plt


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


# calculate average from the input set of images in grayscale
# returns image
def calculate_average_img_grayscale(image_data):
    avg_image = cv2.cvtColor(image_data[0], cv2.COLOR_BGR2GRAY)
    for i in range(len(image_data)):
        if i == 0:
            pass
        else:
            alpha = 1.0 / (i + 1)
            beta = 1.0 - alpha
            avg_image = cv2.addWeighted(cv2.cvtColor(image_data[i], cv2.COLOR_BGR2GRAY), alpha, avg_image, beta, 0.0)
    return avg_image


def calculate_bitwise_or(image_data):
    bitwise_or = cv2.cvtColor(image_data[0], cv2.COLOR_BGR2GRAY)
    for i in range(len(image_data)):
        if i == 0:
            pass
        else:
            grey = cv2.cvtColor(image_data[i], cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(grey, (15, 15), 2)
            bitwise_or = cv2.bitwise_or(bitwise_or, blur)
    return bitwise_or


# subtract one image from another
def subtract_images(img1, img2):
    if img1.shape != img2.shape:
        return 0
    return img1 - img2


def grayscale_numpy_images(images):
    result = []
    for image in images:
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        result.append(grey)
    cv2.imshow('cv2 mean', result[0])

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return np.array(result)


def calculate_median_img(images):
    position_pix = np.zeros(10, dtype=numpy.uint8)
    # median_img = np.zeros((images.shape[1], images.shape[2]), np.int8)
    # mean_img = np.zeros((images.shape[1], images.shape[2]), np.int64)
    mode_img = np.zeros((images.shape[1], images.shape[2]), np.int64)
    for w in range(images.shape[2]):
        for h in range(images.shape[1]):
            for i in range(images.shape[0]):
                position_pix[i] = images[i][h][w]
            # mean_img[h, w] = int(statistics.mean(position_pix)) mean_img.astype(dtype=np.int8),
            mode_img[h, w] = int(statistics.mode(position_pix))
    return mode_img.astype(dtype=np.int8)


def calculate_mode_img(images):
    mode_val = {}
    mode_img = np.zeros((images.shape[1], images.shape[2]), np.uint8)
    for w in range(images.shape[2]):
        for h in range(images.shape[1]):
            for i in range(images.shape[0]):
                if mode_val.get(images[i][h][w]) is None:
                    mode_val.update({images[i][h][w]: 0})
                else:
                    mode_val.update({images[i][h][w]: mode_val.get(images[i][h][w]) + 1})
            mode_img[h, w] = max(mode_val, key=mode_val.get)
            mode_val.clear()
    return mode_img


def calculate_mean_img(images):
    mean_sum = 0
    mean_img = np.zeros((images.shape[1], images.shape[2]), np.uint8)
    for w in range(images.shape[2]):
        for h in range(images.shape[1]):
            for i in range(images.shape[0]):
                mean_sum += images[i][h][w]
            mean_img[h, w] = mean_sum / images.shape[0]
            mean_sum = 0
    return mean_img


# todo
def adaptive_gaussian_thresholding(image, max_val: int):
    img = cv2.medianBlur(image, 5)
    ret, th1 = cv2.threshold(img, max_val - 3, 255, cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    titles = ['Original Image', 'Global Thresholding (v = 127)',
              'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
    images = [img, th1, th2, th3]
    for i in range(4):
        plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()


def binary_thresholding(image, max_val: int):
    print(max_val)
    #plt.imshow(image, 'gray')
    thresh1, image = cv2.threshold(image, 3, 255, cv2.THRESH_BINARY)
    image = 255-image
    plt.imshow(image, 'gray')
    plt.show()
    return image


def extract_template(ref_images):
    # img_data = load_images()
    # img_data_greyscale = grayscale_numpy_images(img_data)
    # mode = calculate_mode_img(img_data_greyscale)
    # mean = calculate_mean_img(img_data_greyscale)
    mean = cv2.imread('../data/results/extracting_template_out/mean.png', cv2.IMREAD_GRAYSCALE)
    mode = cv2.imread('../data/results/extracting_template_out/mode.png', cv2.IMREAD_GRAYSCALE)

    #(thresh, bw_mean_thresh) = cv2.threshold(255 - mean, 80, 255, cv2.THRESH_TOZERO)
    #(thresh1, bw_mode_thresh) = cv2.threshold(255 - mode, 80, 255, cv2.THRESH_TOZERO)

    #bw_mean_thresh_filter = 255 - bw_mean_thresh
    #bw_mode_thresh_filter = 255 - bw_mode_thresh
    #cv2.filterSpeckles(bw_mode_thresh_filter, 255, 1, 1)
    #cv2.filterSpeckles(mode, 255, 1, 1)
    return mode


def draw_contours(img_gray):
    ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
    # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    # draw contours on the original image
    cv2.drawContours(image=img_gray, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                     lineType=cv2.LINE_AA)
    return img_gray


def isolated_pix_remove(image):
    cv2.filterSpeckles(image, 255, 0, 2000)
    return image

    """
    cv2.imwrite('../data/results/extracting_template_out/bw_mean_thresh_filter.png', bw_mean_thresh_filter)
    cv2.imwrite('../data/results/extracting_template_out/bw_mode_thresh_filter.png', bw_mode_thresh_filter)
    #subtraction on images
    subtr_img = subtract_images(gray1, gray2)

    #bitwise operation on gray images
    bitwiseAnd = cv2.bitwise_and(gray1, gray2)
    bitwiseOr = cv2.bitwise_or(gray1, gray2)
    bitwiseXor = cv2.bitwise_xor(gray1, gray2)

    cv2.imshow('bitwise And image', bitwiseAnd)
    cv2.imshow('bitwise Or image', bitwiseOr)
    cv2.imshow('bitwise Xor image', bitwiseXor)

    cv2.imshow('Black white image', blackAndWhiteImage)
    cv2.imshow('Black white image', calculate_bitwise_or(img_data))
    """
