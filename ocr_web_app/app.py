from flask import Flask, request, render_template, redirect, url_for, jsonify
import pytesseract
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    text = None
    if request.method == 'POST':
        file = request.files.get('image')
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            img = Image.open(filepath)
            text = pytesseract.image_to_string(img)
    return render_template('index.html', text=text)


@app.route('/webcam')
def webcam():
    """Serve the webcam OCR page."""
    return render_template('webcam.html')


@app.route('/api/ocr', methods=['POST'])
def api_ocr():
    """Receive an image via POST and return extracted text as JSON."""
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'no image'}), 400
    img = Image.open(file.stream)
    text = pytesseract.image_to_string(img)
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
