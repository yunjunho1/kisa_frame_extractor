from config import make_parser
import glob
import cv2

args = make_parser()


def proc(args, videos):
    vidcap = cv2.VideoCapture(vid)
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    print(fps)

videos_ = glob.glob(f"{args.video_path}/*/*/*.mp4")

videos = []
for vid in videos_:
    proc(args, vid)
