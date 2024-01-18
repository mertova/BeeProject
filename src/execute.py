import argparse
from pathlib import Path
import template_extraction as te
from utils import picture_utils, sift_transformator
from classes.reference import Reference

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--path_reference", help="Path to the reference file")
parser.add_argument("-o", "--path_output", help="Path to the output file for storing template")
parser.add_argument("-d", "--path_data_sample", help="Path to the data sample file")
parser.add_argument("-ev", "--epsilon_vertical", help="Epsilon - deviation for a vertical grid lines")
parser.add_argument("-eh", "--epsilon_horizontal", help="Epsilon - deviation for a horizontal grid lines")
parser.add_argument("-t", "--transform", action="store_true",
                    help="Pick if you want to proceed with transformation of sample data")
parser.add_argument("-p", "--pen_elimination", action="store_true",
                    help="Eliminate (blue) pen handwriting from reference image before transformation, for cleaner "
                         "feature mapping")
args = parser.parse_args()

reference_dir = Path(args.path_reference)
out_dir = Path(args.path_output)
data_sample_dir = Path(args.path_data_sample)

if not out_dir.exists():
    print("The template_out directory doesn't exist\n")
    raise SystemExit(1)

if not data_sample_dir.exists():
    print("The data_sample directory doesn't exist\n")
    raise SystemExit(1)

if not reference_dir.is_file():
    print("The reference file doesn't exist\n")
    raise SystemExit(1)


if __name__ == '__main__':
    reference = Reference(reference_dir)
    if args.pen_elimination:
        print("Removing pen ...\n")
        ref_img_grey = picture_utils.pen_elimination(reference.image_color)
    else:
        print("Skip pen elimination ...\n")
        ref_img_grey = reference.image_grey

    if args.transform:
        print("2D transformation of images ...\n")
        transformed_dir = te.transform_dataset_grey(reference.image_grey, data_sample_dir, out_dir)
    else:
        print("Skip transformation. Data sample directory is used as a transformation directory.\n")
        transformed_dir = data_sample_dir

    te.extract_template(reference, transformed_dir, out_dir, "template-LHI")
