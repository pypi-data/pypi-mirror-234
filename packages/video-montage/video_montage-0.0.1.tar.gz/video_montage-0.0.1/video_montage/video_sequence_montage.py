from tap import Tap
from typing import Optional
import moviepy.editor as mp
import pathlib
from video_montage.utils import create_video_clips, datetime_str


class ArgumentParser(Tap):
    input_video_folder_path: pathlib.Path
    output_video_folder_path: pathlib.Path = pathlib.Path(".")
    output_video_filename: str = f"{datetime_str()}_video_sequence_montage.mp4"
    max_n_videos: Optional[int] = None
    fps: Optional[int] = None


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
    video_sequence = mp.concatenate_videoclips(video_clips, method="compose")

    output_filepath = args.output_video_folder_path / args.output_video_filename
    fps = args.fps if args.fps is not None else video_clips[0].fps
    video_sequence.write_videofile(
        str(output_filepath),
        fps=fps,
    )


if __name__ == "__main__":
    main()
