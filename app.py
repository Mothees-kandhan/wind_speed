from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

rfr = joblib.load('wind_speed_rfr.pkl')

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
        prediction=round(prediction, 3)
        return jsonify({'prediction': prediction})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
