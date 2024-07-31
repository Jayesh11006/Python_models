from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load('game_recommendation_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    print("Received request data:", data)  # Debugging line

    try:
        hardware_specs = np.array([
            data['cpu_score'],
            data['gpu_score'],
            data['ram_size'],
            data['storage_size']
        ]).reshape(1, -1)

        prediction = model.predict(hardware_specs)[0]
        performance_map = {0: 'low', 1: 'medium', 2: 'high'}
        recommendation = performance_map[prediction]
        return jsonify({'recommendation': recommendation})

    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
