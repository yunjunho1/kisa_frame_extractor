import os
import glob
from config import make_parser

args = make_parser()

X = glob.glob(f"{args.output_dir}/*/*/*.jpg")
print(len(X))
