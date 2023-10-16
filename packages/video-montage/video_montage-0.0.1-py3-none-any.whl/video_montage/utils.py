import moviepy.editor as mp
import pathlib
from typing import List, Optional
from datetime import datetime
from functools import lru_cache


@lru_cache()
def datetime_str() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def create_video_clips(
    input_video_folders_path: pathlib.Path, max_n_videos: Optional[int] = None
) -> List[mp.VideoFileClip]:
    VIDEO_EXTENSIONS = ["*.mp4", "*.webm", "*.avi", "*.mov", "*.mkv", "*.gif"]

    video_file_paths = sum(
        [
            list(input_video_folders_path.glob(video_extension))
            for video_extension in VIDEO_EXTENSIONS
        ],
        [],
    )

    max_n_videos = max_n_videos if max_n_videos is not None else len(video_file_paths)
    selected_video_file_paths = video_file_paths[:max_n_videos]

    video_clips = [
        mp.VideoFileClip(str(video_file_path))
        for video_file_path in selected_video_file_paths
    ]
    return video_clips
