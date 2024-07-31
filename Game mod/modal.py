# app.py

from flask import Flask, render_template, request
import pandas as pd
from sklearn.externals import joblib

app = Flask(__name__)

# Load the trained model
model = joblib.load('path_to_your_trained_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get user input from form
        features = [float(x) for x in request.form.values()]
        # Convert to DataFrame
        input_data = pd.DataFrame([features], columns=['Genre', 'Platform', 'Critic_Score', 'User_Score', 'Global_Sales'])
        # Make prediction
        prediction = model.predict(input_data)
        predicted_requirements = prediction[0]
        return render_template('index.html', prediction_text='Predicted System Requirements: {}'.format(predicted_requirements))

if __name__ == '__main__':
    app.run(debug=True)
