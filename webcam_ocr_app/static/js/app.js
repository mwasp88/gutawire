const video = document.getElementById('video');
const output = document.getElementById('ocr-output');
const toggleBtn = document.getElementById('toggle-ocr');
let ocrEnabled = true;
let recognizing = false;

async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        console.error('Could not access webcam:', err);
    }
}

async function captureFrame() {
    if (!ocrEnabled || recognizing) return;
    recognizing = true;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const data = canvas.toDataURL('image/png');

    Tesseract.recognize(data, 'eng', { logger: m => console.log(m) })
        .then(({ data: { text } }) => {
            if (text.trim()) {
                output.textContent = text;
            } else {
                output.textContent = 'No word detected.';
            }
        })
        .catch(err => {
            console.error(err);
            output.textContent = 'No word detected.';
        })
        .finally(() => {
            recognizing = false;
        });
}

function toggleOCR() {
    ocrEnabled = !ocrEnabled;
    toggleBtn.textContent = ocrEnabled ? 'Disable OCR' : 'Enable OCR';
}

toggleBtn.addEventListener('click', toggleOCR);

startCamera().then(() => {
    setInterval(captureFrame, 2000); // capture every 2 seconds
});
