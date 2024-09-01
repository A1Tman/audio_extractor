import subprocess
import sys
import os
import logging
from datetime import datetime

def setup_logging(input_video):
    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Create log file name based on the current time and input file name
    log_file_name = f"logs/{datetime.now().strftime('%Y-%m-%d-%H-%M')}-{os.path.basename(input_video)}.log"
    
    # Setup logging configuration
    logging.basicConfig(
        filename=log_file_name,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Log the start of the operation
    logging.info(f"Starting audio extraction for file: {input_video}")

def extract_audio(input_video, output_audio, format):
    try:
        if format == 'm4a-aac':
            command = ['ffmpeg', '-i', input_video, '-vn', '-acodec', 'aac', '-b:a', '320k', output_audio]
        elif format == 'm4a-alac':
            command = ['ffmpeg', '-i', input_video, '-vn', '-acodec', 'alac', output_audio]
        elif format == 'flac':
            command = ['ffmpeg', '-i', input_video, '-vn', '-acodec', 'flac', output_audio]
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        subprocess.run(command, check=True)
        logging.info(f"Successfully extracted audio in {format}")
        print(f"Successfully extracted audio in {format.split('-')[-1].upper()}")
    except subprocess.CalledProcessError as e:
        error_message = f"An error occurred while running ffmpeg: {e}"
        logging.error(error_message)
        print("Error: Could not extract audio due to a processing error.")
        sys.exit(1)
    except ValueError as ve:
        logging.error(f"Error: {ve}")
        print(f"Error: {ve}")
        sys.exit(1)
    except Exception as ex:
        logging.error(f"An unexpected error occurred: {ex}")
        print("Error: An unexpected error occurred.")
        sys.exit(1)

def main():
    try:
        # Ask the user for the input file path
        input_video = input("Please enter the path to the video file: ").strip()

        # Check if the file exists
        if not os.path.isfile(input_video):
            raise FileNotFoundError(f"The file '{input_video}' does not exist.")

        # Setup logging
        setup_logging(input_video)

        # Ask the user to choose the output format
        print("Choose the output format:")
        print("1: m4a-aac (Lossy, high quality)")
        print("2: m4a-alac (Lossless, high quality)")
        print("3: flac (Lossless, high quality)")

        format_choice = input("Enter the number corresponding to the desired format: ")

        if format_choice == '1':
            format = 'm4a-aac'
            output_ext = '.m4a'
        elif format_choice == '2':
            format = 'm4a-alac'
            output_ext = '.m4a'
        elif format_choice == '3':
            format = 'flac'
            output_ext = '.flac'
        else:
            raise ValueError("Invalid choice. Please enter 1, 2, or 3.")

        # Determine the output file path
        output_audio = os.path.splitext(input_video)[0] + output_ext

        # Handle spaces in file paths by surrounding with quotes
        input_video = f'"{input_video}"'
        output_audio = f'"{output_audio}"'

        # Extract audio
        extract_audio(input_video, output_audio, format)

    except FileNotFoundError as fnf_error:
        logging.error(f"Error: {fnf_error}")
        print("Error: The specified file does not exist.")
        sys.exit(1)
    except ValueError as ve:
        logging.error(f"Error: {ve}")
        print(f"Error: {ve}")
        sys.exit(1)
    except Exception as ex:
        logging.error(f"An unexpected error occurred: {ex}")
        print("Error: An unexpected error occurred.")
        sys.exit(1)

if __name__ == "__main__":
    main()
