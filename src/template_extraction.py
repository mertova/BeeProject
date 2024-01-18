import cv2
from classes.reference import Reference
from classes.template import Template
from utils import picture_utils, sift_transformator
from pathlib import Path


def transform_dataset_grey(reference_grey: cv2.Mat, data_sample_dir: Path, template_out_dir: Path):
    print("loading images from {}".format(data_sample_dir), "\n")
    images = picture_utils.load_data_grey(data_sample_dir)

    if images is None or len(images) == 0:
        print("empty directory of source images\n")
        return

    transform_dir = template_out_dir / "transformed"
    transform_dir.mkdir(exist_ok=True)
    i = 0
    print("transforming images ... \n")
    for img in images:
        transformed = sift_transformator.map_img_to_ref(img.copy(), reference_grey)
        img_path = transform_dir / (i.__str__() + ".png")
        cv2.imwrite(img_path.as_posix(), transformed)
        print("transformed image {}\n".format(img_path.as_posix()))
        i += 1
    print("\ntransformed all images\n")


def extract_template(reference: Reference, data_samples_dir: Path, results_dir: Path, template_name: str):
    images = picture_utils.load_data_grey(data_samples_dir)

    if images is None or len(images) == 0:
        print("empty directory of images\n")
        return

    images.append(reference.image_grey)

    # todo finish for some templates it might be essential
    subt = picture_utils.calculate_subtracted_img(images)
    cv2.imwrite(results_dir.as_posix() + "subtr.png", subt)

    average = picture_utils.calculate_average_img(images)
    cv2.imwrite(results_dir.as_posix() + "average.png", average)

    subt_image = cv2.bitwise_not(images[0])
    thresh, bw_mean_thresh = cv2.threshold(subt_image, 60, 255, cv2.THRESH_TOZERO)
    bw_mean_thresh_filter = 255 - bw_mean_thresh

    cv2.filterSpeckles(bw_mean_thresh_filter, 255, 10, 2000)
    cv2.imwrite(results_dir.as_posix() + "bw_mean_thresh_speckles.png", bw_mean_thresh_filter)

    template_clean = picture_utils.gamma_correction(bw_mean_thresh_filter)
    cv2.imwrite(results_dir.as_posix() + template_name, template_clean)
    return Template(template_name, results_dir / template_name, template_clean)
