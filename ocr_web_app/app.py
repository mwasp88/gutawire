from flask import Flask, request, render_template, redirect, url_for
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
