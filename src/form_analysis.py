from pathlib import Path

import cv2

from image_processing.reference import Reference


class FormAnalysis:
    def __init__(self, out_dir: Path, ref_img):
        self.reference = Reference(ref_img)
        self.out_dir = out_dir

    def extract(self, data_sample_dir: Path, limit: int, debug: bool, transform: bool, averaging: bool):
        """
        identify the template from the sample data and reference image based on the comon and overlapping pixels
        :return: tuple: recognized template image, average overlapping pixels, and threshold image
        """

        if data_sample_dir is None or not data_sample_dir.exists():
            print("Path does not exist")
            raise SystemExit(1)

        self.reference.pen_elimination()
        pen_eliminated = self.reference.get_color()

        if averaging:
            self.averaging(data_sample_dir, limit, transform)
        self.reference.clean_averaged_form()
        if debug:
            self._dump_debug_images([pen_eliminated, self.reference.get_grey()])
        else:
            cv2.imwrite((self.out_dir / "mask.png").as_posix(), self.reference.get_color())
        return self.reference.get_grey()

    def averaging(self, data_sample_dir: Path, limit: int, transform: bool):
        print("averaging sample data ...")
        p = data_sample_dir.glob('**/*.png')
        i = 0
        for x in p:
            if x.is_file() and i < limit:
                scan = cv2.imread(x.as_posix(), cv2.IMREAD_GRAYSCALE)
                if transform:
                    print("transformed image ", i, ": ", x.stem)
                    scan = self.reference.map_img_to_ref(scan)
                self.reference.add_weighted(scan)
                i += 1

        print("cleaning form ...")

    def _dump_debug_images(self, images):
        debug_dir = self.out_dir / 'debug' / 'templates/'
        debug_dir.mkdir(parents=True, exist_ok=True)
        i = 0
        for img in images:
            file_path = debug_dir / Path(str(i) + ".png")
            if img is not None:
                cv2.imwrite(file_path.as_posix(), img)
            i += 1
