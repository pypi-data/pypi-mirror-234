from tap import Tap
from typing import Optional, List
import moviepy.editor as mp
import pathlib
import math
from video_montage.utils import create_video_clips, datetime_str


class ArgumentParser(Tap):
    input_video_folder_path: pathlib.Path
    output_video_folder_path: pathlib.Path = pathlib.Path(".")
    output_video_filename: str = f"{datetime_str()}_video_grid_montage.mp4"
    max_n_videos: Optional[int] = None
    max_duration_seconds: Optional[int] = None
    fps: Optional[int] = None
    num_per_row: Optional[int] = None


def trim_video_clips(
    video_clips: List[mp.VideoFileClip], max_duration_seconds: Optional[int] = None
) -> List[mp.VideoFileClip]:
    shortest_duration_seconds = min([video_clip.duration for video_clip in video_clips])
    montage_duration_seconds = (
        min(shortest_duration_seconds, max_duration_seconds)
        if max_duration_seconds is not None
        else shortest_duration_seconds
    )
    video_clips = [
        video_clip.subclip(0, montage_duration_seconds) for video_clip in video_clips
    ]
    return video_clips


def main() -> None:
    args: ArgumentParser = ArgumentParser().parse_args()
    assert (
        args.input_video_folder_path.exists()
    ), f"Input video folder path {args.input_video_folder_path} does not exist."

    if not args.output_video_folder_path.exists():
        print(f"Creating output folder {args.output_video_folder_path}")
        args.output_video_folder_path.mkdir(parents=True)

    video_clips = create_video_clips(
        args.input_video_folder_path, max_n_videos=args.max_n_videos
    )
    video_clips = trim_video_clips(
        video_clips, max_duration_seconds=args.max_duration_seconds
    )

    DEFAULT_NUM_PER_ROW = math.ceil(math.sqrt(len(video_clips)))
    num_per_row = (
        args.num_per_row if args.num_per_row is not None else DEFAULT_NUM_PER_ROW
    )
    num_rows = math.ceil(len(video_clips) / num_per_row)
    video_grid = mp.clips_array(
        [video_clips[i * num_per_row : (i + 1) * num_per_row] for i in range(num_rows)]
    )

    output_filepath = args.output_video_folder_path / args.output_video_filename
    fps = args.fps if args.fps is not None else video_clips[0].fps
    video_grid.write_videofile(
        str(output_filepath),
        fps=fps,
    )


if __name__ == "__main__":
    main()
