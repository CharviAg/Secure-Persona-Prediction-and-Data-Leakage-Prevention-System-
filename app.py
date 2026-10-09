
import streamlit as st

st.title("Customer Persona Analytics")

try:
    from database import login_user
    st.success("database.py loaded successfully")
except Exception as e:
    st.error(f"Database Error: {e}")

try:
    from predict_persona import predict_cluster
    st.success("predict_persona.py loaded successfully")
except Exception as e:
    st.error(f"Prediction Error: {e}")