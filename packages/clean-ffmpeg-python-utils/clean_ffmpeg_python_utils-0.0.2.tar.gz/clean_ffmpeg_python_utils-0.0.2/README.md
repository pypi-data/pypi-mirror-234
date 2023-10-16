# clean_ffmpeg_python_utils

Easy-to-use ffmpeg python utils with simpler arguments

# Installing

Install:

```
pip install clean_ffmpeg_python_utils
```

# Usage

```
clean_ffmpeg_python_utils --help

usage: clean_ffmpeg_python_utils --input_filepath INPUT_FILEPATH [--output_extension OUTPUT_EXTENSION] [--output_filepath OUTPUT_FILEPATH] [--fps FPS]
                           [--start_time START_TIME] [--duration DURATION] [--width WIDTH] [--height HEIGHT] [-h]

optional arguments:
  --input_filepath INPUT_FILEPATH
                        (Path, required)
  --output_extension OUTPUT_EXTENSION
                        (Union[str, NoneType], default=None)
  --output_filepath OUTPUT_FILEPATH
                        (Union[pathlib.Path, NoneType], default=None)
  --fps FPS             (Union[int, NoneType], default=None)
  --start_time START_TIME
                        (Union[int, NoneType], default=None)
  --duration DURATION   (Union[int, NoneType], default=None)
  --width WIDTH         (Union[int, NoneType], default=None)
  --height HEIGHT       (Union[int, NoneType], default=None)
  -h, --help            show this help message and exit
```

# Example 1: Convert mp4 to gif

```
clean_ffmpeg_python_utils --input_filepath openai_rubiks_cube.mp4 --output_extension gif
```

# Example 2: Trim video length

```
clean_ffmpeg_python_utils --input_filepath openai_rubiks_cube.mp4 --start_time 25 --duration 10
```

# Example 3: Modify FPS

```
clean_ffmpeg_python_utils --input_filepath openai_rubiks_cube.mp4 --fps 10
```
