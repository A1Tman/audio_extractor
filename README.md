# Audio Extractor GUI

I needed to extract audio from video files regularly. Existing tools were either command-line only or bloated. This is a straightforward PyQt5 GUI wrapper around FFmpeg that handles the most common use cases.

## What it does

- Extracts audio from video files using FFmpeg
- Supports `m4a-aac` (lossy), `m4a-alac` (lossless), and `flac` (lossless) output formats
- Automatically logs all operations to `logs/` directory
- Runs on Windows, macOS, and Linux

## Requirements

- Python 3.6+
- FFmpeg (must be in system PATH)

## Installation

Clone and install dependencies:

```bash
git clone https://github.com/A1Tman/audio_extractor
cd audio_extractor
pip install -r requirements.txt
```

Install FFmpeg:

**Ubuntu:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

## Running the application

```bash
python audio_extractor_gui.py
```

## Creating a standalone executable

If you prefer a double-clickable executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed audio_extractor_gui.py
```

The executable will be in the `dist/` directory.

## Usage

1. Run the application
2. Browse for your video file
3. Select output format from dropdown
4. Click "Extract Audio"
5. Check the logs if anything goes wrong

The extracted audio file will be saved in the same directory as the source video.

## Contributing

Fork, make changes, submit pull request. Standard procedure.

## License

MIT License. See LICENSE file.
