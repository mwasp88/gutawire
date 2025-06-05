# gutawire

This repository now includes a simple webcam-based OCR application built with Flask and JavaScript.

## Webcam OCR App

The app connects to your webcam, displays the live feed, and extracts any visible text using `tesseract.js`. Results are shown in real time next to the video stream.

### Running the App

1. Install dependencies:
   ```bash
   pip install -r webcam_ocr_app/requirements.txt
   ```
2. Start the Flask server:
   ```bash
   python webcam_ocr_app/app.py
   ```
3. Open your browser to `http://localhost:5000` and allow webcam access.

Use the toggle button to enable or disable OCR processing.
