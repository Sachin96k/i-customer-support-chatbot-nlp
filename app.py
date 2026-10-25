"""Flask web application for the NLP customer support chatbot."""
import json
import random
import re
from pathlib import Path

import joblib
from flask import Flask, jsonify, render_template, request

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "intent_model.joblib"
INTENTS_PATH = ROOT / "intents.json"
CONFIDENCE_THRESHOLD = 0.30

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

def load_intents():
    with INTENTS_PATH.open(encoding="utf-8") as file:
        return {item["tag"]: item for item in json.load(file)["intents"]}

INTENTS = load_intents()
MODEL = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None

def clean_text(text):
    """Lightweight normalization; TF-IDF handles tokenization and features."""
    return re.sub(r"\s+", " ", text.strip())

def get_reply(message):
    message = clean_text(message)
    if not message:
        return {"reply": "Please type a message so I can help.", "intent": "empty", "confidence": 0.0}

    if MODEL is None:
        return {"reply": "The chatbot model has not been trained yet. Please run `python train.py` and restart the app.", "intent": "model_missing", "confidence": 0.0}

    probabilities = MODEL.predict_proba([message])[0]
    best_index = probabilities.argmax()
    intent = MODEL.classes_[best_index]
    confidence = float(probabilities[best_index])

    if confidence < CONFIDENCE_THRESHOLD:
        intent = "unknown"

    intent_data = INTENTS.get(intent, INTENTS["unknown"])
    reply = random.choice(intent_data["responses"])
    return {"reply": reply, "intent": intent, "confidence": round(confidence, 3)}

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    if not isinstance(message, str):
        return jsonify({"error": "Message must be text."}), 400
    if len(message) > 1000:
        return jsonify({"error": "Please keep messages under 1000 characters."}), 400
    return jsonify(get_reply(message))

@app.get("/health")
def health():
    return jsonify({"status": "ok", "model_loaded": MODEL is not None})

if __name__ == "__main__":
    # Debug mode is useful locally. Do not expose this development server publicly.
    app.run(host="127.0.0.1", port=5000, debug=True)
