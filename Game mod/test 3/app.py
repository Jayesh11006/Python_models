from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)

# Load the games dataset and the trained model
games_df = pd.read_csv('games.csv')
model = joblib.load('game_recommendation_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    print("Received request data:", data)  # Debugging line

    try:
        cpu_score = data['cpu_score']
        gpu_score = data['gpu_score']
        ram_size = data['ram_size']
        storage_size = data['storage_size']

        # Filter games based on hardware specs
        filtered_games = games_df[
            (games_df['cpu_score'] <= cpu_score) &
            (games_df['gpu_score'] <= gpu_score) &
            (games_df['ram_size'] <= ram_size) &
            (games_df['storage_size'] <= storage_size)
        ]

        recommended_games = filtered_games['game_name'].tolist()
        return jsonify({'recommended_games': recommended_games})

    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
