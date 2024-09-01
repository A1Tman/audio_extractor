# Audio Extractor GUI

Audio Extractor GUI is a user-friendly tool built with PyQt5 that allows you to extract audio from video files with ease. The application supports output formats `m4a-aac`, `m4a-alac`, and `flac`.

## Features

- **Simple and Intuitive GUI**: Built with PyQt5.
- **Audio Formats**: Supports `m4a-aac` (lossy), `m4a-alac` (lossless), and `flac` (lossless) audio formats.
- **Logging**: Automatically generates logs for each extraction, stored in the `logs/` directory.
- **Cross-Platform**: Can be run on Windows, macOS, and Linux.

## Installation

### Prerequisites

- **Python 3.6+**: Ensure that Python is installed on your system.
- **ffmpeg**: The `ffmpeg` tool is required for extracting audio.

### Steps to Install

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/A1Tman/audio_extractor
    cd audio_extractor
    ```

2. **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Ensure `ffmpeg` is Installed**:
    - On **Ubuntu**:
        ```bash
        sudo apt-get install ffmpeg
        ```
    - On **macOS** (using Homebrew):
        ```bash
        brew install ffmpeg
        ```
    - On **Windows**:
        - Download `ffmpeg` from the [official site](https://ffmpeg.org/download.html) and add it to your system's PATH.

4. **Run the Application**:
    ```bash
    python audio_extractor_gui.py
    ```

### Optional: Create an Executable

To create a standalone executable that can be run by double-clicking:

1. **Install PyInstaller**:
    ```bash
    pip install pyinstaller
    ```

2. **Create the Executable**:
    ```bash
    pyinstaller --onefile --windowed audio_extractor_gui.py
    ```

3. **Locate the Executable**:
    - The executable will be in the `dist/` directory. You can double-click to run it.

## Usage

1. **Open the Application**: Double-click the executable or run the script using Python.

2. **Select a Video File**: Click on "Browse" to select the video file you want to extract audio from.

3. **Choose the Output Format**: Select the desired audio format from the dropdown menu (`m4a-aac`, `m4a-alac`, `flac`).

4. **Extract Audio**: Click "Extract Audio" to start the extraction process. A log file will be generated in the `logs/` directory.

5. **View Results**: Once completed, a message will confirm whether the extraction was successful.

## Contributing

Contributions are welcome! If you would like to contribute, please fork the repository, create a new branch, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **PyQt5**: For the amazing GUI framework.
- **ffmpeg**: The powerful multimedia framework used for audio extraction.
- **Python**: The programming language that made this project possible.
