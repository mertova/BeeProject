import cv2
import glob


# import all image files with the .png extension
def load_images():
    images = glob.glob("examples/transformedQuality/*.png")
    image_data = []
    for img in images:
        this_image = cv2.imread(img, 1)
        image_data.append(this_image)
    return image_data


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
    bitwise_or = cv2.cvtColor(img_data[0], cv2.COLOR_BGR2GRAY)
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


img_data = load_images()
#cv2.imwrite('out/extracting_template_out/average_img.png', calculate_average_img(img_data))
#cv2.imwrite('out/extracting_template_out/average_gray_img.png', calculate_average_img_grayscale(img_data))


"""
gray1 = cv2.cvtColor(img_data[0], cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img_data[1], cv2.COLOR_BGR2GRAY)
"""

"""
#subtraction on images
subtr_img = subtract_images(gray1, gray2)
cv2.imshow('Original image 1',img_data[0])
cv2.imshow('Original image 2',img_data[1])
cv2.imshow('subtracted image', subtr_img)
"""

"""
#bitwise operation on gray images
bitwiseAnd = cv2.bitwise_and(gray1, gray2)
bitwiseOr = cv2.bitwise_or(gray1, gray2)
bitwiseXor = cv2.bitwise_xor(gray1, gray2)

cv2.imshow('bitwise And image', bitwiseAnd)
cv2.imshow('bitwise Or image', bitwiseOr)
cv2.imshow('bitwise Xor image', bitwiseXor)
"""
grayAverageImage = calculate_average_img_grayscale(img_data)

grayAverageImage = (255-grayAverageImage)
(thresh, blackAndWhiteImage) = cv2.threshold(grayAverageImage, 80, 255, cv2.THRESH_TOZERO)
blackAndWhiteImage = (255-blackAndWhiteImage)

#cv2.imshow('Black white image', blackAndWhiteImage)

cv2.imshow('Black white image', calculate_bitwise_or(img_data))

cv2.waitKey(0)
cv2.destroyAllWindows()




#cv2.imwrite("out/extracting_template_out/average_blured3.png", blackAndWhiteImage)

#cv2.imwrite('out/average.png', calculate_average_img(img_data))