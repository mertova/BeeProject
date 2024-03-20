from pathlib import Path

import cv2

from extraction.template import Template
from transformator import sift_transformator
from utils.image_utils import calculate_average, adjust_gamma, pen_elimination


def load_sample_data_grey(data_sample_dir, limit):
    if data_sample_dir is None or not data_sample_dir.exists():
        print("Path does not exist")
        raise SystemExit(1)

    p = data_sample_dir.glob('**/*.png')
    i = 0
    image_data = []
    for x in p:
        if x.is_file() and i < limit:
            image_data.append((cv2.imread(x.as_posix(), cv2.IMREAD_GRAYSCALE), x.as_posix()))
    return image_data


class TemplateExtraction:
    def __init__(self, out_dir: Path, reference: Path):
        self.reference = cv2.imread(reference.as_posix())
        self.template_dir = out_dir / 'template.png'
        self.debug_dir = out_dir / 'debug_templates/'

    def process_pipeline(self, data_sample):
        pen_eliminated = pen_elimination(self.reference)
        average = calculate_average(pen_eliminated, data_sample)
        img_not = cv2.bitwise_not(average)
        thresh, bw_mean_thresh = cv2.threshold(img_not, 60, 255, cv2.THRESH_TOZERO)
        bw_mean_thresh_filter = 255 - bw_mean_thresh
        cv2.filterSpeckles(bw_mean_thresh_filter, 255, 10, 2000)
        template_clean = adjust_gamma(bw_mean_thresh_filter, 2)
        return template_clean, average, bw_mean_thresh_filter

    def dump_debug_images(self, images):
        self.debug_dir.mkdir(parents=True, exist_ok=True)
        i = 0
        for img in images:
            file_path = self.debug_dir / Path(str(i) + ".png")
            cv2.imwrite(file_path.as_posix(), img)
            i += 1

    def extract(self, data_sample_dir, limit, transform: bool, debug: bool):
        """
        identify the template from the sample data and reference image based on the comon and overlapping pixels
        :return: tuple: recognized template image, average overlapping pixels, and threshold image
        """
        if self.reference is None:
            print("No reference found")
            exit(1)
        data_sample = load_sample_data_grey(data_sample_dir, limit)
        if data_sample is None or len(data_sample) == 0:
            print("Empty sample images\n")
            exit(1)

        transformed_images = []
        i = 0
        if transform:
            print("transforming sample data ...")
            for img in data_sample:
                transformed = sift_transformator.map_img_to_ref(img[0],
                                                                cv2.cvtColor(self.reference, cv2.COLOR_BGR2GRAY))
                transformed_images.append(transformed)
                print("transformed image ", i, "\n", img[1])
                i += 1
            if debug:
                self.dump_debug_images(transformed_images)
            data_sample = transformed_images

        print("Extracting template ...")
        template, average, bw_mean_thresh_filter = self.process_pipeline(data_sample)

        if debug:
            self.dump_debug_images([template, average, bw_mean_thresh_filter])
        return Template(self.template_dir, template)

    def get_template_from_reference(self):
        return Template(self.template_dir, self.reference)
