import os
from config import make_parser
import cv2
import numpy as np
import pandas as pd
from multiprocessing import Process
import glob

args = make_parser()

def time_converter(x, fps):
    x = str(x).split(":")
    x = int(x[0])*3600+int(x[1])*60+int(x[2])
    x = x*fps
    
    return x

def proc(args, videos, labels):
    for vid in videos:
        task = vid.split("/")[-2]
        vid_name = vid.split("/")[-1].split(".mp4")[0]
    
        labels_ = labels[labels["video_name"]==vid.split("/")[-1]]
        start = labels_["start"].item()
        end = labels_["end"].item()
        N_ = labels_["N"].item()
        stride = int((end-start)/N_)

        cand = np.arange(start, end, stride)
        cand = np.random.choice(cand, size=N_, replace=False)

        vidcap = cv2.VideoCapture(vid)
    
        fid = 0 
        while True:
            uccess, image = vidcap.read()
            if fid in cand:
                save_path = f"{args.output_dir}/{task}/{vid_name}"
                os.makedirs(save_path, exist_ok=True)
                cv2.imwrite(f"{save_path}/{fid}.jpg", image)
            fid+=1 
            if fid > end:
                break

labels = pd.read_csv("labels.csv")

new_labels = pd.DataFrame(None, columns=["video_name", "start", "end", "N"])
for i in range(len(labels)):
    vname = labels.iloc[i]["video_name"]
    start = time_converter(labels.iloc[i]["start"], args.fps)
    end = time_converter(labels.iloc[i]["end"], args.fps)
    N = end-start
    new_labels.loc[i] = [vname, start, end, N]
n = args.n_samples/len(new_labels)
df1 = new_labels[new_labels["N"]<n]
remain = args.n_samples-np.sum(df1["N"])
df2 = new_labels[new_labels["N"]>=n]
n = int(remain/len(df2))
df2["N"] = n
labels = pd.concat((df1, df2)).reset_index()


target_vd = labels["video_name"].tolist()
videos_ = glob.glob(f"{args.video_path}/*/*/*.mp4")

videos = []
for vid in videos_:
    if vid.split("/")[-1] in target_vd:
        videos.append(vid)
print(f"total videos : {len(videos_)}, Fails : {len(videos)}")

procs = []

split = np.array_split(videos, args.core)
for index, videos in enumerate(split):
    p = Process(target=proc, args=(args, videos, labels))
    procs.append(p)
    p.start()

for p in procs:
    p.join()
