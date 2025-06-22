from flask import Flask, send_from_directory, request, jsonify, Response
import json
import serial
import cv2

# Use the default video device. On Raspberry Pi this is usually `/dev/video0`

SERIAL_PORT = "/dev/serial0"  # Raspberry Pi UART
SERIAL_BAUD = 9600
serial_conn = None

print(f"[INFO] Using serial port: {SERIAL_PORT} @ {SERIAL_BAUD} baud")

app = Flask(__name__, static_folder=".")

def gen_frames():
    """Generator yielding camera frames as JPEG bytes."""
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("[ERROR] Camera not available")
        return
    try:
        while True:
            success, frame = cam.read()
            if not success:
                print("[ERROR] Failed to read frame")
                break
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        cam.release()

def get_serial_connection():
    global serial_conn
    if serial_conn is not None:
        return serial_conn
    try:
        serial_conn = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1)
        print(f"[OK] Serial connection established on {SERIAL_PORT}")
    except Exception as e:
        print(f"[ERROR] Could not open serial port {SERIAL_PORT}: {e}")
        serial_conn = None
    return serial_conn

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/serial_event', methods=['POST'])
def serial_event():
    data = request.get_json(force=True, silent=True)
    if not isinstance(data, dict):
        return jsonify({'status': 'error', 'message': 'Invalid JSON'}), 400

    ser = get_serial_connection()

    if ser:
        try:
            json_data = json.dumps(data) + '\n'
            ser.write(json_data.encode('utf-8'))
            print(f"[>] Sent to serial: {json_data.strip()}")
        except Exception as e:
            print(f"[ERROR] Failed to write to serial: {e}")
            return jsonify({'status': 'error', 'message': 'Serial write failed'}), 500
    else:
        print("[!] No serial connection. Fallback to console.")
        print("Serial output:", json.dumps(data))

    return jsonify({'status': 'ok'})

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
