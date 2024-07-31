from flask import Flask, request, jsonify, send_from_directory
import cv2
import mediapipe as mp
import os

app = Flask(__name__)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

@app.route('/')
def home():
    return "Hand Sign Detection Server is Running"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['image']
    file.save('input.jpg')
    image = cv2.imread('input.jpg')
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)

    response = {"jutsu": "none"}
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Detect specific hand signs here and set jutsu
            pass

    return jsonify(response)

if __name__ == '__main__':
    app.run()
