from flask import Flask, request, jsonify, render_template_string
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib

app = Flask(__name__)

# Load the label encoder for the target variable
label_encoder = LabelEncoder()
try:
    label_encoder = joblib.load('label_encoder.pkl')
except Exception as e:
    print(f"Error loading label encoder: {e}")

# Load the saved model
try:
    best_model = joblib.load('trained_model.pkl')
except Exception as e:
    print(f"Error loading model: {e}")

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Obesity Prediction</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>Obesity Prediction</h1>
        <form id="prediction-form" action="/predict" method="GET">
            <label for="gender">Gender:</label>
            <select class="input" name="gender" id="gender">
                <option value="Male">Male</option>
                <option value="Female">Female</option>
            </select><br>

            <label for="age">Age:</label>
            <input class="input" type="number" name="age" id="age" required><br>

            <label for="height">Height (Meters):</label>
            <input class="input" type="number" name="height" id="height" step="0.01" required><br>

            <label for="weight">Weight (KG):</label>
            <input class="input" type="number" name="weight" id="weight" required><br>

            <label for="family_history">Family History with Overweight:</label>
            <select class="input" name="family_history" id="family_history">
                <option value="yes">Yes</option>
                <option value="no">No</option>
            </select><br>

            <label for="favc">FAVC (High Caloric Food):</label>
            <select class="input" name="favc" id="favc">
                <option value="yes">Yes</option>
                <option value="no">No</option>
            </select><br>

            <label for="fcvc">FCVC (Vegetable Consumption):</label>
            <input class="input" type="number" name="fcvc" id="fcvc" step="0.01" required><br>

            <label for="ncp">NCP (Number of Meals):</label>
            <input class="input" type="number" name="ncp" id="ncp" step="0.01" required><br>

            <label for="caec">CAEC (Food Consumption between Meals):</label>
            <select class="input" name="caec" id="caec">
                <option value="no">No</option>
                <option value="Sometimes">Sometimes</option>
                <option value="Frequently">Frequently</option>
                <option value="Always">Always</option>
            </select><br>

            <label for="smoke">Smoke:</label>
            <select class="input" name="smoke" id="smoke">
                <option value="no">No</option>
                <option value="yes">Yes</option>
            </select><br>

            <label for="ch2o">CH2O (Water Intake):</label>
            <input class="input" type="number" name="ch2o" id="ch2o" step="0.01" required><br>

            <label for="scc">SCC (Monitoring of Calories):</label>
            <select class="input" name="scc" id="scc">
                <option value="no">No</option>
                <option value="yes">Yes</option>
            </select><br>

            <label for="faf">FAF (Physical Activity Frequency):</label>
            <input class="input" type="number" name="faf" id="faf" step="0.01" required><br>

            <label for="tue">TUE (Time using Technology Devices):</label>
            <input class="input" type="number" name="tue" id="tue" step="0.01" required><br>

            <label for="calc">CALC (Alcohol Consumption):</label>
            <select class="input" name="calc" id="calc">
                <option value="no">No</option>
                <option value="Sometimes">Sometimes</option>
                <option value="Frequently">Frequently</option>
                <option value="Always">Always</option>
            </select><br>

            <label for="mtrans">MTRANS (Transportation):</label>
            <select class="input" name="mtrans" id="mtrans">
                <option value="Automobile">Automobile</option>
                <option value="Bike">Bike</option>
                <option value="Motorbike">Motorbike</option>
                <option value="Public_Transportation">Public Transportation</option>
                <option value="Walking">Walking</option>
            </select><br>

            <div class="btn">
                <button type="submit">Predict</button>
                <div class="popup" id="popup">
                    <img src="{{ url_for('static', filename='img/Techno_india_logo.jpg') }}" alt="Techno India Logo">
                    <h2 id="result">Prediction Result</h2>
                    <button type="button" onclick="closePopup()">OK</button>
                </div>
            </div>
        </form>
    </div>
    <div class="popup" id="popup">
        <img src="{{ url_for('static', filename='img/Techno_india_logo.jpg') }}" alt="Techno India Logo">
        <h2 id="result">Prediction Result</h2>
        <button type="button" onclick="closePopup()">OK</button>
    </div>
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/predict', methods=['GET'])
def predict():
    try:
        # Retrieve data from request.args for GET method
        gender = request.args.get('gender')
        age = float(request.args.get('age', 0))  # Default to 0 if empty or None
        height = float(request.args.get('height', 0))
        weight = float(request.args.get('weight', 0))
        family_history = request.args.get('family_history', '')
        favc = request.args.get('favc', '')
        fcvc = float(request.args.get('fcvc', 0))
        ncp = float(request.args.get('ncp', 0))
        caec = request.args.get('caec', '')
        smoke = request.args.get('smoke', '')
        ch2o = float(request.args.get('ch2o', 0))
        scc = request.args.get('scc', '')
        faf = float(request.args.get('faf', 0))
        tue = float(request.args.get('tue', 0))
        calc = request.args.get('calc', '')
        mtrans = request.args.get('mtrans', '')

        # Prepare input data
        input_data = pd.DataFrame({
            'Gender': [gender],
            'Age': [age],
            'Height': [height],
            'Weight': [weight],
            'family_history_with_overweight': [family_history],
            'FAVC': [favc],
            'FCVC': [fcvc],
            'NCP': [ncp],
            'CAEC': [caec],
            'SMOKE': [smoke],
            'CH2O': [ch2o],
            'SCC': [scc],
            'FAF': [faf],
            'TUE': [tue],
            'CALC': [calc],
            'MTRANS': [mtrans]
        })

        # Make prediction using the loaded model
        prediction = best_model.predict(input_data)
        result = label_encoder.inverse_transform(prediction)[0]
        return jsonify(result=result)
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
