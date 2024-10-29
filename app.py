from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load model and label encoder
model = joblib.load('iris_model.joblib')
label_encoder = joblib.load('label_encoder.joblib')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get values from form
        culmen_length = float(request.form['culmen_length'])
        culmen_depth = float(request.form['culmen_depth'])
        flipper_length = float(request.form['flipper_length'])
        body_mass = float(request.form['body_mass'])

        # Prepare data for prediction
        input_data = pd.DataFrame({
            'Culmen Length (mm)': [culmen_length],
            'Culmen Depth (mm)': [culmen_depth],
            'Flipper Length (mm)': [flipper_length],
            'Body Mass (g)': [body_mass]
        })

        # Make prediction
        prediction = model.predict(input_data)
        predicted_species = label_encoder.inverse_transform(prediction)

        return jsonify({
            'prediction': predicted_species[0]
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
