# -*- coding:utf-8 -*-
from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips
from skimage.feature import hog
from sklearn.cluster import KMeans
import numpy as np
import os
import time

def scene_splitter(video_path, n_clusters=1, frame_rate=1):
    print("Load video")
    video = VideoFileClip(video_path)
    
    print("Extract frames from video")
    frames = [frame for frame in video.iter_frames(fps=frame_rate, dtype=np.uint8)]
    
    print("Compute HOG features for each frame")
    hog_features = [hog(frame, pixels_per_cell=(16, 16), cells_per_block=(2, 2), visualize=False,channel_axis=2) for frame in frames]
    
    print("Cluster frames using KMeans")
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(hog_features)
    
    print("Identify scene changes based on cluster transitions")
    labels = kmeans.labels_
    scene_changes = [0] + [i for i in range(1, len(labels)) if labels[i] != labels[i-1]] + [len(labels)]
    
    print("Convert frame indices to time")
    scene_changes_time = [change / frame_rate for change in scene_changes]
    
    print("Split video into scenes")
    scene_clips = [video.subclip(start_t, min(end_t, video.duration)) for start_t, end_t in zip(scene_changes_time[:-1], scene_changes_time[1:])]
        
    return scene_clips

def get_first_frames(videoclips):
    frames = []
    for clip in videoclips:
        frames.append(clip.get_frame(0))
    return frames

def concatenate_and_save_video(file_path,videoclips):
    processed_video = concatenate_videoclips(videoclips)
    processed_video.write_videofile(os.path.dirname(file_path)+ "\\"+ time.strftime('%Y-%m-%d_%H-%M-%S')+"_output_video.mp4")
