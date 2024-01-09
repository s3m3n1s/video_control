import cv2

from flask import render_template, Response
from app import app


@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    video_capture = cv2.VideoCapture(0)
    while True:
        success, frame = video_capture.read()

        if not success:
            break

        # Преобразование кадра в формат JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Генерация кадра для передачи в видеопоток
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    # Возвращаем Response с функцией генерации кадров в формате multipart
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
