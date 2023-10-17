# shrinktunes

`shrinktunes` is a convenience wrapper for `ffmpeg` batch jobs. It was originally created for batch converting audio files in a large asset library to various formats, containers, and compression levels.

## Usage

Once installed, you can use the `shrinktunes` command to convert files specified individually or with a glob pattern. Below are some examples.

### Convert a Single File

```bash
shrinktunes convert "path/to/your/file.wav" -o mp3
```

### Convert Files to Multiple Formats

```bash
shrinktunes convert "path/to/your/files/*.wav" -o mp3 -o ogg
```

### Convert with Verbose Logging

```bash
shrinktunes convert -v "path/to/your/files/*.wav" -o mp3
```

### Force Overwrite Existing Files

```bash
shrinktunes convert "path/to/your/files/*.wav" -o mp3 -f
```

## Installation

You'll need to have [`FFmpeg`](https://ffmpeg.org) installed on your machine to use shrinktunes. If you don't have it installed, the CLI will provide instructions on how to get it based on your platform.

This project uses `poetry` for dependency management and packaging. To install shrinktunes, first [get poetry](https://python-poetry.org/docs/#installation), then run:

```bash
poetry install
```

## Commands

### `shrinktunes convert`

- `<glob_pattern>`: A **quoted** glob pattern for files to convert, e.g. `"path/to/your/files/*.wav"

  (**Note**: If you forget to quote it, it won't be interpreted as a glob, but rather expanded by your shell, which will likely result in an error.`)
- `-o <ext>`: Output format by file extension; must be specified one or more times. Supported formats are dynamically determined from `ffmpeg` (see `shrinktunes info` for common formats or `ffmpeg -formats` for all of them).
- `-v`: Enable verbose logging mode
- `-f`: Force overwrite of existing files

### `shrinktunes info`

You can also use shrinktunes to print information about the available codecs on your system with the `info` command:

```bash
$ shrinktunes info
ffmpeg is installed

Decoders:
aac                  raw ADTS AAC (Advanced Audio Coding)
avi                  AVI (Audio Video Interleaved)
flac                 raw FLAC
m4a                  QuickTime / MOV
mp3                  MP3 (MPEG audio layer 3)
mp4                  QuickTime / MOV
ogg                  Ogg
wav                  WAV / WAVE (Waveform Audio)
webm                 Matroska / WebM

Encoders:
avi                  AVI (Audio Video Interleaved)
flac                 raw FLAC
mp3                  MP3 (MPEG audio layer 3)
mp4                  MP4 (MPEG-4 Part 14)
ogg                  Ogg
wav                  WAV / WAVE (Waveform Audio)
webm                 WebM
```

**Note** It currently filters down to a few common ones (let me know of obvious oversights).

Use `ffmpeg -formats` to see the full list (they will still work with `shrinktunes` if ffmpeg can do it; the list is just overwhelmingly long so we have made it short).

## Development

Clone the repository and install the dependencies with Poetry:

```bash
git clone https://github.com/your-username/shrinktunes.git
cd shrinktunes
poetry install
```

### Tests

Tests utilize `pytest`. After installing the dependencies, run the tests with:

```bash
poetry run pytest
```

Or, inside a venv like I do:

```bash
$ source .venv/bin/activate
(shrinktunes) $ pytest
```

### Contributing

We welcome contributions! Please open an issue or submit a pull request on GitHub.

### License

`shrinktunes` is open-source software, released under [MIT License](LICENSE).

### Author

[Brian Jorgensen](https://github.com/b33j0r)
