import pandas as pd
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_FILE = os.path.join(BASE_DIR, "data", "prediction_history.csv")
def save_prediction(customer_id, income, spending_score, persona):
    new_record = pd.DataFrame({
        "CustomerID": [customer_id],
        "Income": [income],
        "SpendingScore": [spending_score],
        "Persona": [persona]
    })
    file_exists = os.path.exists(HISTORY_FILE)
    new_record.to_csv(
        HISTORY_FILE,
        mode="a",
        header=not file_exists,
        index=False
    )
def get_prediction_history():
    if not os.path.exists(HISTORY_FILE):
        return pd.DataFrame(
            columns=[
                "CustomerID",
                "Income",
                "SpendingScore",
                "Persona"
            ]
        )
    return pd.read_csv(HISTORY_FILE)
