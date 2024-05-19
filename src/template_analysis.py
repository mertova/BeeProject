from pathlib import Path

import cv2
from image_processing.reference import Reference


class TemplateExtraction:
    def __init__(self, out_dir: Path, ref_img):
        self.reference = Reference(ref_img)
        self.template_dir = out_dir / 'template.png'
        self.debug_dir = out_dir / 'debug_templates/'

    def extract(self, data_sample_dir: Path, limit: int, debug: bool):
        """
        identify the template from the sample data and reference image based on the comon and overlapping pixels
        :return: tuple: recognized template image, average overlapping pixels, and threshold image
        """

        if data_sample_dir is None or not data_sample_dir.exists():
            print("Path does not exist")
            raise SystemExit(1)

        self.reference.pen_elimination()

        print("averaging sample data ...")
        p = data_sample_dir.glob('**/*.png')
        i = 0
        avg_image = self.reference.grey
        for x in p:
            if x.is_file() and i < limit:
                scan = cv2.imread(x.as_posix(), cv2.IMREAD_GRAYSCALE)
                transformed = self.reference.map_img_to_ref(scan)
                alpha = 1.0 / (i + 1)
                beta = 1.0 - alpha
                avg_image = cv2.addWeighted(transformed, alpha, avg_image, beta, 1.0)
                i += 1
                print("transformed image ", i, ": ", x.stem)

        print("Extracting template ...")
        average, bw_mean_thresh_filter = self.reference.clean_image()

        if debug:
            self.dump_debug_images([self.reference.grey, average, bw_mean_thresh_filter])
        return self.reference.grey

    def dump_debug_images(self, images):
        self.debug_dir.mkdir(parents=True, exist_ok=True)
        i = 0
        for img in images:
            file_path = self.debug_dir / Path(str(i) + ".png")
            cv2.imwrite(file_path.as_posix(), img)
            i += 1
