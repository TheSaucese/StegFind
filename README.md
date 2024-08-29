
# StegFind - Steganography Detection Tool

## Overview
**StegFind** is a robust tool designed to detect and analyze hidden data in various file formats such as images, audio, and video files. It combines a variety of methods to provide comprehensive steganography detection, surpassing traditional tools by offering features like LSB detection, StegHide, OutGuess detection, and more.

## Key Features
- **LSB Detection**: Detect hidden data in images by analyzing least significant bits.
- **StegHide Detection**: Identify files concealed using StegHide, even without a passphrase.
- **OutGuess Detection**: Detect data hidden with OutGuess in various file types.
- **Embedded Files Handling**: Extract embedded or hidden files within target data.
- **EXIF Data Analysis**: Analyze EXIF data in images for embedded information.
- **Spectrogram Analysis**: For audio files, visualize frequency content to detect hidden messages.
- **Hexdump and Strings Analysis**: Examine file contents in hexadecimal or string format to uncover hidden data.

## How to Run StegFind

### Prerequisites
- Python 3.x
- Flask and other necessary Python libraries.

First, install the required Python packages using pip. You can usually find a `requirements.txt` file in the root directory of the project. Run the following command in your terminal:
```bash
pip install -r requirements.txt
```

### Running the Application
1. Run the Flask application with:
   ```bash
   python app.py
   ```
2. Open a web browser and access the application at `http://127.0.0.1:5000/`.
3. Upload the file you want to analyze using the web interface.
4. View the results directly in your browser.
