import cv2
import mediapipe as mp
import numpy as np
import pyautogui
from flask import Flask, render_template, redirect, url_for, session
from flask_socketio import SocketIO, emit
import face_recognition
import os

app = Flask(__name__)
app.secret_key = 'super secret key'
socketio = SocketIO(app)

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()
face_verified = False

@app.route('/')
def index():
    if face_verified:
        return redirect(url_for('home'))
    else:
        return render_template('not_safe.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/verify')
def verify():
    return render_template('verify.html')

def capture_face():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face_image = frame[y:y + h, x:x + w]
            cv2.imwrite('registered_face.jpg', face_image)
            cap.release()
            cv2.destroyAllWindows()
            return redirect(url_for('index'))

        cv2.imshow('Face Registration', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def verify_face():
    global face_verified
    cap = cv2.VideoCapture(0)
    registered_image = face_recognition.load_image_file('registered_face.jpg')
    registered_encoding = face_recognition.face_encodings(registered_image)[0]

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces([registered_encoding], face_encoding)
            if True in matches:
                face_verified = True
                cap.release()
                cv2.destroyAllWindows()
                return redirect(url_for('index'))

        cv2.imshow('Face Verification', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def detect_face_and_hands():
    global face_verified
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                x, y = int(index_finger_tip.x * screen_width), int(index_finger_tip.y * screen_height)
                pyautogui.moveTo(x, y)

                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                distance = np.sqrt((index_finger_tip.x - thumb_tip.x) ** 2 + (index_finger_tip.y - thumb_tip.y) ** 2)
                if distance < 0.05:
                    pyautogui.click()

                socketio.emit('hand_data', {'landmarks': str(hand_landmarks)})

        cv2.imshow('Face and Hand Detection', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    if not os.path.exists('registered_face.jpg'):
        capture_face()
    else:
        verify_face()

    from threading import Thread
    thread = Thread(target=detect_face_and_hands)
    thread.start()
    socketio.run(app, debug=True)
