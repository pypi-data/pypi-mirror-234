# video_montage

Easily create a video montage (either a sequence or a grid of videos)

# Installing

Install:

```
pip install video_montage
```

# Usage

Before running, you must have a prepare an input video folder with videos the following structure, eg.

```
<INPUT_VIDEO_FOLDER_PATH>
├── <video1>.mp4
├── <video2>.mp4
└── ...
```

`video_grid_montage`: Create a grid of videos (all playing at the same time)

```
video_grid_montage --help

usage: video_grid_montage --input_video_folder_path INPUT_VIDEO_FOLDER_PATH [--output_video_folder_path OUTPUT_VIDEO_FOLDER_PATH]
                          [--output_video_filename OUTPUT_VIDEO_FILENAME] [--max_n_videos MAX_N_VIDEOS]
                          [--max_duration_seconds MAX_DURATION_SECONDS] [--fps FPS] [--num_per_row NUM_PER_ROW] [-h]

optional arguments:
  --input_video_folder_path INPUT_VIDEO_FOLDER_PATH
                        (Path, required)
  --output_video_folder_path OUTPUT_VIDEO_FOLDER_PATH
                        (Path, default=.)
  --output_video_filename OUTPUT_VIDEO_FILENAME
                        (str, default=2023-10-07_18-58-19_video_grid_montage.mp4)
  --max_n_videos MAX_N_VIDEOS
                        (Union[int, NoneType], default=None)
  --max_duration_seconds MAX_DURATION_SECONDS
                        (Union[int, NoneType], default=None)
  --fps FPS             (Union[int, NoneType], default=None)
  --num_per_row NUM_PER_ROW
                        (Union[int, NoneType], default=None)
  -h, --help            show this help message and exit
```

`video_sequence_montage`: Create a sequence of videos (playing one at a time sequentially)

```
video_sequence_montage --help

usage: video_sequence_montage --input_video_folder_path INPUT_VIDEO_FOLDER_PATH [--output_video_folder_path OUTPUT_VIDEO_FOLDER_PATH]
                              [--output_video_filename OUTPUT_VIDEO_FILENAME] [--max_n_videos MAX_N_VIDEOS] [--fps FPS] [-h]

optional arguments:
  --input_video_folder_path INPUT_VIDEO_FOLDER_PATH
                        (Path, required)
  --output_video_folder_path OUTPUT_VIDEO_FOLDER_PATH
                        (Path, default=.)
  --output_video_filename OUTPUT_VIDEO_FILENAME
                        (str, default=2023-10-07_18-58-59_video_sequence_montage.mp4)
  --max_n_videos MAX_N_VIDEOS
                        (Union[int, NoneType], default=None)
  --fps FPS             (Union[int, NoneType], default=None)
  -h, --help            show this help message and exit
```

# Example Usage

```
(video_montage_env) ➜  video_montage git:(main) ✗ tree openai_rubiks_cube 

openai_rubiks_cube
├── 2023-10-07_20-04-36_openai_rubiks_cube.gif
├── 2023-10-07_20-05-13_openai_rubiks_cube.gif
├── 2023-10-07_20-05-48_openai_rubiks_cube.gif
├── 2023-10-07_20-07-27_openai_rubiks_cube.gif
├── 2023-10-07_20-08-02_openai_rubiks_cube.gif
└── 2023-10-07_20-11-18_openai_rubiks_cube.gif

0 directories, 6 files
(video_montage_env) ➜  video_montage git:(main) ✗ video_grid_montage --input_video_folder_path openai_rubiks_cube
Moviepy - Building video 2023-10-07_20-16-08_video_grid_montage.mp4.
Moviepy - Writing video 2023-10-07_20-16-08_video_grid_montage.mp4

Moviepy - Done !
Moviepy - video ready 2023-10-07_20-16-08_video_grid_montage.mp4
```