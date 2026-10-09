"""
predict persona
Loads the pre-trained model + scaler (from train_model.py) and exposes:

    predict_cluster(age, gender, income, spending_score) -> int
    predict_persona(age, gender, income, spending_score) -> (int, str)

If the saved model files are missing (or cannot be loaded because of a
scikit-learn version change) the model is trained again automatically.
"""

import os
import json
import pickle
import numpy as np

import train_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "kmeans_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")
MAP_PATH = os.path.join(BASE_DIR, "cluster_persona_map.json")


def _load():
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        with open(SCALER_PATH, "rb") as f:
            scaler = pickle.load(f)
        with open(MAP_PATH) as f:
            persona_map = {int(k): v for k, v in json.load(f).items()}
        return model, scaler, persona_map
    except Exception:
        model, scaler, persona_map, _ = train_model.train()
        return model, scaler, persona_map


# Load once at import time (not on every call)
_kmeans_model, _scaler, _persona_map = _load()


def predict_cluster(age: float, gender: str, income: float, spending_score: float) -> int:
    """
    Returns the predicted cluster number.

    gender: "Male" or "Female"
    income: same units as the training data (Rs. thousands)
    spending_score: 1-100
    """
    gender_encoded = 0 if str(gender).strip().lower() == "male" else 1

    input_data = np.array([[age, gender_encoded, income, spending_score]], dtype=float)
    scaled_input = _scaler.transform(input_data)

    return int(_kmeans_model.predict(scaled_input)[0])


def predict_persona(age, gender, income, spending_score):
    """Returns (cluster, persona name)."""
    cluster = predict_cluster(age, gender, income, spending_score)
    return cluster, _persona_map.get(cluster, "Unknown Persona")


if __name__ == "__main__":
    print(predict_persona(25, "Female", 60, 75))
