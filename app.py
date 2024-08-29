from flask import Flask, request, render_template, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

with open('wind_speed_rfr.pkl', 'rb') as file:
    rfr = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        input_data = {
            'IND': data.get('IND'),
            'RAIN': data.get('RAIN'),
            'IND.1': data.get('IND1'),
            'T.MAX': data.get('TMAX'),
            'IND.2': data.get('IND2'),
            'T.MIN': data.get('TMIN'),
            'T.MIN.G': data.get('TMIN_G'),
            'MONTH': data.get('MONTH')
        }

        df = pd.DataFrame([input_data])

        prediction = rfr.predict(df)[0]

        return jsonify({'prediction': prediction})

    except Exception as e:
        return jsonify({'error': str(e)})
