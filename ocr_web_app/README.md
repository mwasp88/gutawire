# OCR Web App

This is a simple Flask-based web application that lets you upload an image and extracts text from it using Tesseract OCR.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python app.py
   ```

Open your browser at `http://localhost:5000` and upload an image to see the extracted text.

## Webcam OCR via Browser

Navigate to `http://localhost:5000/webcam` to allow the page to access your webcam. The page will automatically capture a frame every few seconds and display any detected words.

## Live Webcam OCR

You can also read text from your webcam in real time. To start the webcam OCR viewer run:

```bash
python webcam_ocr.py
```

A window will open showing your webcam feed with detected words overlaid. Press `q` to quit.
