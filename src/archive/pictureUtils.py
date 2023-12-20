import cv2
import statistics
import numpy as np
from matplotlib import pyplot as plt


# expects all images same shape!
def sum_canny(images: list):
    if (images is None) or (len(images) == 0):
        return None

    # Second, process edge detection use Canny.
    low_threshold = 50
    high_threshold = 300
    sum_image = images[0] * 0

    kernel_size = 5

    for image in images:
        edges = cv2.Canny(cv2.GaussianBlur(image, (kernel_size, kernel_size), 0), low_threshold, high_threshold)
        thresh1, edges = cv2.threshold(edges, 127, 1, cv2.THRESH_BINARY)
        sum_image += edges

    return sum_image, len(images)


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


# Function to map each intensity level to output intensity level.
def pixelVal(pix, r1, s1, r2, s2):
    if (0 <= pix and pix <= r1):
        return (s1 / r1) * pix
    elif (r1 < pix and pix <= r2):
        return ((s2 - s1) / (r2 - r1)) * (pix - r1) + s1
    else:
        return ((255 - s2) / (255 - r2)) * (pix - r2) + s2


def calculate_median_img(images):
    position_pix = np.zeros(10, dtype=np.uint8)
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
# must be grey
def adaptive_gaussian_thresholding(image, max_val: int):
    inverse = cv2.bitwise_not(image)
    img = cv2.medianBlur(inverse, 5)
    ret, th1 = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
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
    return img, th1, th2, th3


def draw_contours(img_gray):
    ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
    # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    # draw contours on the original image
    cv2.drawContours(image=img_gray, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                     lineType=cv2.LINE_AA)
    return img_gray


def extract_template_mode(template, images):
    if images is None or len(images) == 0:
        print("empty directory of images")
        return

    mode = calculate_mode_img(images)
    cv2.imwrite("mode.png", mode)
    mean = calculate_mean_img(images)

    thresh, bw_mean_thresh = cv2.threshold(255 - mean, 80, 255, cv2.THRESH_TOZERO)
    thresh1, bw_mode_thresh = cv2.threshold(255 - mode, 80, 255, cv2.THRESH_TOZERO)

    bw_mean_thresh_filter = 255 - bw_mean_thresh
    cv2.imwrite("mode_postprocessing.png", bw_mean_thresh_filter)

    bw_mode_thresh_filter = 255 - bw_mode_thresh
    cv2.filterSpeckles(bw_mode_thresh_filter, 255, 1, 1)
    cv2.filterSpeckles(mode, 255, 1, 1)
    cv2.imwrite("bw_mode_thresh_filter.png", bw_mode_thresh_filter)
    cv2.imwrite("mode_speckless.png", mode)

    template_grey = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    cv2.filterSpeckles(template_grey, 255, 1000, 2000)
    cv2.imwrite("template_clean.png", template_grey)
