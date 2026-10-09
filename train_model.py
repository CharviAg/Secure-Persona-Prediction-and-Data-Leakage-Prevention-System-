"""
train model
Trains a K-Means clustering model on customer data and saves it
(along with the fitted scaler and the cluster -> persona map)
so main.py can load it at runtime without retraining.
"""

import os
import json
import pickle
from itertools import permutations

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "Mall_Customers.csv")
MODEL_PATH = os.path.join(BASE_DIR, "kmeans_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")
MAP_PATH = os.path.join(BASE_DIR, "cluster_persona_map.json")

# The app has 4 personas, so the model uses 4 clusters
OPTIMAL_K = 4
PERSONAS = [
    "High-Value Customer",
    "Budget Customer",
    "Potential Customer",
    "Impulsive Spender",
]


def build_persona_map(kmeans, scaler):
    """Give each cluster a persona by looking at its centre (income vs spending)."""
    centers = scaler.inverse_transform(kmeans.cluster_centers_)  # Age, Gender, Income, Spending
    income = centers[:, 2]
    spend = centers[:, 3]
    inc_z = (income - income.mean()) / (income.std() or 1)
    sp_z = (spend - spend.mean()) / (spend.std() or 1)

    # score of each cluster for each persona
    scores = {
        "High-Value Customer": inc_z + sp_z,       # high income, high spending
        "Budget Customer": -inc_z - sp_z,          # low income, low spending
        "Potential Customer": inc_z - sp_z,        # high income, low spending
        "Impulsive Spender": sp_z - inc_z,         # high spending relative to income
    }

    best_total, best_perm = None, None
    for perm in permutations(range(OPTIMAL_K)):    # perm[i] = cluster given to PERSONAS[i]
        total = sum(scores[PERSONAS[i]][perm[i]] for i in range(OPTIMAL_K))
        if best_total is None or total > best_total:
            best_total, best_perm = total, perm

    return {int(best_perm[i]): PERSONAS[i] for i in range(OPTIMAL_K)}


def train(make_plot=False):
    # 1. Load dataset
    df = pd.read_csv(DATA_PATH)

    df.rename(columns={
        "Annual Income (Rs. Thousands)": "Annual_Income",
        "Annual Income (k$)": "Annual_Income",
        "Spending Score (1-100)": "Spending_Score",
    }, inplace=True)

    # 2. Preprocess  (Male -> 0, Female -> 1)
    df["Gender"] = df["Gender"].map({"Male": 0, "Female": 1})
    df = df.dropna(subset=["Age", "Gender", "Annual_Income", "Spending_Score"])

    features = df[["Age", "Gender", "Annual_Income", "Spending_Score"]].values
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # 3. Elbow method (only when run directly)
    if make_plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        inertias = []
        K_range = range(1, 11)
        for k in K_range:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            km.fit(scaled_features)
            inertias.append(km.inertia_)

        plt.figure(figsize=(8, 5))
        plt.plot(K_range, inertias, marker="o")
        plt.xlabel("Number of clusters (k)")
        plt.ylabel("Inertia")
        plt.title("Elbow Method for Optimal k")
        plt.savefig(os.path.join(BASE_DIR, "elbow_plot.png"))
        plt.close()
        print("Elbow plot saved as elbow_plot.png")

    # 4. Train final K-Means model
    kmeans = KMeans(n_clusters=OPTIMAL_K, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(scaled_features)

    persona_map = build_persona_map(kmeans, scaler)

    # 5. Save model + scaler + persona map
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(kmeans, f)
    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)
    with open(MAP_PATH, "w") as f:
        json.dump(persona_map, f, indent=2)

    return kmeans, scaler, persona_map, df


if __name__ == "__main__":
    _, _, persona_map, data = train(make_plot=True)
    print("Cluster counts:")
    print(data["Cluster"].value_counts())
    print("Cluster -> Persona:", persona_map)
    print("Model, scaler and persona map saved.")
