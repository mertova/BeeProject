import glob
import line_recognition
import cv2
import os
from sift_transformator import map_img_to_ref

documents_dir = '../data/scans/png/Sample-JKI-BS/'
results_transformed_dir = '../data/results/transformedQuality/'
ref_img_path = '../data/scans/template-empty.png'


def main():
    images = glob.glob(documents_dir + "*.png")
    image_data = []

    ref_image = cv2.imread(ref_img_path)

    for img in images:
        image_cv2 = cv2.imread(img, 1)
        image_data.append(image_cv2)
        transformed = map_img_to_ref(image_cv2, ref_image,
                                 MIN_MATCH_COUNT=10)



    
def transform():
    # Reading in the reference image using OpenCV
    ref_image_cv2 = cv2.imread(ref_img_path)
    # Analyse all the images in the 'images_dir' path
    with os.scandir(documents_dir) as img_iterator:
        for image in img_iterator:
            # Skipping files that are not in the formats PNG, JPG or JPEG
            if not (image.name.endswith('.png') or
                    image.name.endswith('.jpg') or
                    image.name.endswith('.JPG') or
                    image.name.endswith('.jpeg')):
                continue
            image_name = image.name.rsplit('.')[0]
            print(f'\nCurrently processed image: {image_name}')
            # Reading in an image using OpenCV
            image_cv2 = cv2.imread(image.path)
            # Transforming
            transformed = map_img_to_ref(image_cv2, ref_image_cv2,
                                         MIN_MATCH_COUNT=10)
            cv2.imwrite(results_transformed_dir + image_name + '_transformed.png',
                        transformed)


if __name__ == '__main__':
    main()
