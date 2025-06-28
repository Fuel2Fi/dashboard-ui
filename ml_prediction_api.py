from flask import Flask, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)

# Load the trained model (make sure you've saved it before)
model = joblib.load("trained_model.joblib")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    features = np.array(data["features"]).reshape(1, -1)
    prediction = model.predict(features)[0]
    return jsonify({"predicted_price": prediction})

if __name__ == "__main__":
    app.run(port=5000)
