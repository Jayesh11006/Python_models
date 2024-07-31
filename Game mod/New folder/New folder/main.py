from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

app = Flask(__name__)

# Load the trained model
model = joblib.load('game_recommendation_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

app.run(debug=True)
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get user input from form
        memory = int(request.form['memory'])
        graphics_card = request.form['graphics_card']
        os = request.form['os']

        # Encode categorical variables
        label_encoder = LabelEncoder()
        graphics_card_encoded = label_encoder.fit_transform([graphics_card])
        os_encoded = label_encoder.fit_transform([os])

        # Make prediction
        prediction = model.predict([[memory, graphics_card_encoded[0], os_encoded[0]]])[0]
        return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)

