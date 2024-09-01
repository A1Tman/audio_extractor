import sys
import os
import subprocess
import logging
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QFileDialog, QMessageBox, QHBoxLayout, QProgressBar
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal

def setup_logging(input_video):
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    log_file_name = f"logs/{datetime.now().strftime('%Y-%m-%d-%H-%M')}-{os.path.basename(input_video)}.log"
    
    logging.basicConfig(
        filename=log_file_name,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info(f"Starting audio extraction for file: {input_video}")

class WorkerThread(QThread):
    progress = pyqtSignal(int)
    result = pyqtSignal(str)

    def __init__(self, input_video, output_audio, format):
        super().__init__()
        self.input_video = input_video
        self.output_audio = output_audio
        self.format = format

    def run(self):
        print("Worker thread running")  # Debugging line
        try:
            if self.format == 'm4a-aac':
                command = ['ffmpeg', '-i', self.input_video, '-vn', '-acodec', 'aac', '-b:a', '320k', self.output_audio]
            elif self.format == 'm4a-alac':
                command = ['ffmpeg', '-i', self.input_video, '-vn', '-acodec', 'alac', self.output_audio]
            elif self.format == 'flac':
                command = ['ffmpeg', '-i', self.input_video, '-vn', '-acodec', 'flac', self.output_audio]
            else:
                raise ValueError(f"Unsupported format: {self.format}")

            print(f"Running command: {' '.join(command)}")  # Debugging line
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in process.stdout:
                print(line.decode('utf-8').strip())  # Debugging line
                if b'time=' in line:
                    self.progress.emit(50)  # Fake progress update for demonstration
            process.wait()

            if process.returncode == 0:
                self.progress.emit(100)
                logging.info(f"Successfully extracted audio in {self.format}")
                self.result.emit(f"Successfully extracted audio in {self.format.split('-')[-1].upper()}")
            else:
                logging.error(f"Error: ffmpeg failed with return code {process.returncode}")
                self.result.emit("Error: Could not extract audio due to a processing error.")
        except Exception as ex:
            logging.error(f"An unexpected error occurred: {ex}")
            self.result.emit("Error: An unexpected error occurred.")

class AudioExtractorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Audio Extractor')
        self.setWindowIcon(QIcon('icon.png'))

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #25A77A;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1E8C66;
            }
            QComboBox {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QProgressBar {
                text-align: center;
                font-size: 14px;
                color: #333;
                border-radius: 5px;
            }
            QMessageBox QPushButton {
                background-color: #25A77A;
                color: white;
                padding: 5px;
                border-radius: 5px;
            }
        """)

        layout = QVBoxLayout()

        file_layout = QHBoxLayout()
        self.file_label = QLabel('Select video file:')
        self.file_input = QLineEdit(self)
        self.file_input.setPlaceholderText('Click "Browse" to select a video file')
        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.browse_button)
        
        self.format_label = QLabel('Select output format:')
        self.format_combo = QComboBox(self)
        self.format_combo.addItem("m4a-aac (Lossy, high quality)")
        self.format_combo.addItem("m4a-alac (Lossless, high quality)")
        self.format_combo.addItem("flac (Lossless, high quality)")

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)

        button_layout = QHBoxLayout()
        self.extract_button = QPushButton('Extract Audio', self)
        self.extract_button.clicked.connect(self.start_extraction)
        button_layout.addStretch(1)
        button_layout.addWidget(self.extract_button)
        button_layout.addStretch(1)
        
        layout.addLayout(file_layout)
        layout.addWidget(self.format_label)
        layout.addWidget(self.format_combo)
        layout.addWidget(self.progress_bar)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.resize(400, 250) 
        self.setFixedSize(self.size())

    def browse_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.mp4 *.mkv *.avi *.mov);;All Files (*)", options=options)
        if file_path:
            self.file_input.setText(file_path)

    def start_extraction(self):
        print("Start extraction called")  # Debugging line
        input_video = self.file_input.text()
        format_choice = self.format_combo.currentText()

        if not os.path.isfile(input_video):
            print("File does not exist")  # Debugging line
            QMessageBox.critical(self, "Error", "The specified file does not exist.")
            return

        if "m4a-aac" in format_choice:
            format = 'm4a-aac'
            output_ext = '.m4a'
        elif "m4a-alac" in format_choice:
            format = 'm4a-alac'
            output_ext = '.m4a'
        elif "flac" in format_choice:
            format = 'flac'
            output_ext = '.flac'
        else:
            print("Invalid format selected")  # Debugging line
            QMessageBox.critical(self, "Error", "Invalid format selected.")
            return

        output_audio = os.path.splitext(input_video)[0] + output_ext
        setup_logging(input_video)

        self.progress_bar.setValue(0)
        print("Starting worker thread")  # Debugging line

        self.worker = WorkerThread(input_video, output_audio, format)
        self.worker.progress.connect(self.update_progress)
        self.worker.result.connect(self.show_result)
        self.worker.start()
        print("Worker thread started")  # Debugging line

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def show_result(self, message):
        QMessageBox.information(self, "Result", message)
        self.progress_bar.setValue(0)  # Reset the progress bar after completion

def main():
    app = QApplication(sys.argv)
    ex = AudioExtractorGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
