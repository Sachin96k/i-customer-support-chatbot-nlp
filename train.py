"""Train the intent classifier from intents.json and save the model."""
import json
from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "intents.json"
MODEL_DIR = ROOT / "models"
MODEL_PATH = MODEL_DIR / "intent_model.joblib"

def load_training_data():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    texts, labels = [], []
    for intent in data["intents"]:
        # The "unknown" examples are intentionally not used for supervised training:
        # real unknown messages are handled with a confidence threshold in app.py.
        if intent["tag"] == "unknown":
            continue
        for pattern in intent["patterns"]:
            texts.append(pattern)
            labels.append(intent["tag"])
    return texts, labels

def main():
    texts, labels = load_training_data()
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2), strip_accents="unicode")),
        ("classifier", LogisticRegression(max_iter=2000, class_weight="balanced"))
    ])
    pipeline.fit(texts, labels)
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Saved model to: {MODEL_PATH}")
    print(f"Training examples: {len(texts)}")
    print(f"Intent classes: {len(set(labels))}")
    print("Model trained successfully.")
    print("Note: this small demo dataset is for learning, not production accuracy.")

if __name__ == "__main__":
    main()
