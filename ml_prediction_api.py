from flask import Flask, jsonify, request
import numpy as np
import joblib

app = Flask(__name__)

# Dummy balance endpoint
@app.route("/balance", methods=["GET"])
def get_balance():
    return jsonify({"balance": 1234.56})

# Dummy strategy endpoint
@app.route("/strategy", methods=["GET"])
def get_strategy():
    return jsonify({"strategy": "Mean Reversion"})

# Dummy trades endpoint
@app.route("/trades", methods=["GET"])
def get_trades():
    trades = [
        {"time": "2025-06-28 21:00", "symbol": "BTCUSD", "signal": "BUY", "result": "WIN"},
        {"time": "2025-06-28 20:00", "symbol": "ETHUSD", "signal": "SELL", "result": "LOSS"}
    ]
    return jsonify({"trades": trades})

# Existing prediction endpoint
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    model = joblib.load("trained_model.joblib")
    features = np.array(data["features"]).reshape(1, -1)
    prediction = model.predict(features)[0]
    return jsonify({"predicted_price": prediction})

if __name__ == "__main__":
    app.run(port=5000)

