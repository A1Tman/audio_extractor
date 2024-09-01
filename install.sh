#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Check if Python is installed
if ! command_exists python3; then
    echo "Python3 could not be found. Please install Python3 to proceed."
    exit 1
fi

# Check if pip is installed
if ! command_exists pip3; then
    echo "pip3 could not be found. Installing pip3..."
    sudo apt-get install python3-pip -y
fi

# Install Python dependencies (none required in this case)
pip3 install -r requirements.txt

# Check if ffmpeg is installed
if ! command_exists ffmpeg; then
    echo "ffmpeg could not be found. Installing ffmpeg..."
    
    # Detect OS and install ffmpeg
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update
        sudo apt-get install ffmpeg -y
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ffmpeg
    elif [[ "$OSTYPE" == "msys"* ]] || [[ "$OSTYPE" == "cygwin"* ]]; then
        echo "Please download and install ffmpeg from https://ffmpeg.org/download.html for Windows."
        exit 1
    else
        echo "Unsupported OS. Please install ffmpeg manually."
        exit 1
    fi
else
    echo "ffmpeg is already installed."
fi

echo "Environment setup complete."
