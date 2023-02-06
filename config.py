import argparse

def make_parser():
    parser = argparse.ArgumentParser("X")
    parser.add_argument("--video_path", type=str, default="/workspace/data_raw/KISA", help="root_dir for image directory")
    parser.add_argument("--n_samples", default=10000, type=int, help="number of remain images")
    parser.add_argument("--output_dir", type=str, default="/workspace/data_raw/KISA_images2", help="path to save pruned results")
    parser.add_argument("--seed", default=None, type=int)
    parser.add_argument("--core", default=10, type=int)
    parser.add_argument("--fps", default=30, type=int)
    args = parser.parse_args()

    return args