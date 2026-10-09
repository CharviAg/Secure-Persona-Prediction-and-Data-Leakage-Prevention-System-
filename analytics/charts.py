import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "customers.csv")

def income_vs_spending():
    df = pd.read_csv(DATA_FILE)
    plt.figure(figsize=(9, 6))
    personas = df["Persona"].unique()
    for persona in personas:
        persona_data = df[df["Persona"] == persona]
        plt.scatter(
            persona_data["Income"],
            persona_data["SpendingScore"],
            label=persona,
            s=80
        )
    plt.xlabel("Annual Income")
    plt.ylabel("Spending Score")
    plt.title("Income vs Spending Score")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
def persona_distribution():
    df = pd.read_csv(DATA_FILE)
    persona_counts = df["Persona"].value_counts()
    plt.figure(figsize=(9, 6))
    bars = plt.bar(
        persona_counts.index,
        persona_counts.values
    )
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.05,
            str(int(height)),
            ha="center",
            fontsize=12
        )
    plt.xlabel("Customer Persona")
    plt.ylabel("Number of Customers")
    plt.title("Customer Persona Distribution")
    plt.xticks(rotation=20)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    income_vs_spending()
    persona_distribution()
