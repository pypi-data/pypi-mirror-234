from tap import Tap
import ffmpeg
import pathlib
from typing import Optional
from datetime import datetime
from functools import lru_cache


VIDEO_EXTENSIONS = ["mp4", "webm", "avi", "mov", "mkv", "gif"]


@lru_cache()
def datetime_str() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


class ArgumentParser(Tap):
    input_filepath: pathlib.Path
    output_extension: Optional[str] = None
    output_filepath: Optional[pathlib.Path] = None
    fps: Optional[int] = None
    start_time: Optional[int] = None
    duration: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None


def add_datetime_str_to_filename(filepath: pathlib.Path) -> pathlib.Path:
    return filepath.parent / f"{datetime_str()}_{filepath.name}"


def get_output_filepath(args: ArgumentParser) -> pathlib.Path:
    assert (
        args.output_extension is None or args.output_extension in VIDEO_EXTENSIONS
    ), f"Output extension {args.output_extension} is not supported."

    if args.output_filepath is not None and args.output_extension is None:
        return args.output_filepath
    elif args.output_filepath is not None and args.output_extension is not None:
        assert (
            args.output_filepath.suffix == f".{args.output_extension}"
        ), f"Output filepath {args.output_filepath} does not have the correct extension {args.output_extension}."
        return args.output_filepath
    elif args.output_filepath is None and args.output_extension is None:
        return args.input_filepath
    else:
        return (
            args.input_filepath.parent
            / f"{args.input_filepath.stem}.{args.output_extension}"
        )


def main() -> None:
    args: ArgumentParser = ArgumentParser().parse_args()
    assert (
        args.input_filepath.exists()
    ), f"Input path {args.input_filepath} does not exist."

    output_filepath = add_datetime_str_to_filename(get_output_filepath(args))
    print(f"Output filepath: {output_filepath}")
    output_filepath.parent.mkdir(parents=True, exist_ok=True)

    stream = ffmpeg.input(str(args.input_filepath))

    if args.fps is not None:
        stream = ffmpeg.filter(stream, "fps", fps=args.fps, round="up")

    if args.width is not None and args.height is not None:
        stream = ffmpeg.filter(stream, "scale", width=args.width, height=args.height)
    elif args.width is not None:
        stream = ffmpeg.filter(stream, "scale", width=args.width, height=-1)
    elif args.height is not None:
        stream = ffmpeg.filter(stream, "scale", width=-1, height=args.height)

    if args.start_time is not None and args.duration is not None:
        stream = ffmpeg.output(
            stream, str(output_filepath), ss=args.start_time, t=args.duration
        )
    elif args.start_time is not None:
        stream = ffmpeg.output(stream, str(output_filepath), ss=args.start_time)
    elif args.duration is not None:
        stream = ffmpeg.output(stream, str(output_filepath), t=args.duration)
    else:
        stream = ffmpeg.output(stream, str(output_filepath))
    ffmpeg.run(stream)
    print("Done")


if __name__ == "__main__":
    main()
