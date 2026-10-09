
import streamlit as st
import pandas as pd

from database import login_user
from predict_persona import predict_cluster

st.set_page_config(
    page_title="Customer Persona Analytics",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 Customer Persona Analytics")
st.write("Understand customer behaviour and predict customer segments.")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Predict Persona", "About"]
)

if page == "Dashboard":
    st.header("Dashboard")
    st.info("Your customer analytics dashboard will appear here.")

elif page == "Predict Persona":
    st.header("Predict Customer Persona")
    st.write("Enter customer details to predict their persona.")

    col1, col2 = st.columns(2)

    with col1:
        income = st.number_input(
            "Annual Income (k$)", min_value=0.0, value=50.0
        )
        age = st.number_input(
            "Age", min_value=18, max_value=100, value=30
        )

    with col2:
        spending = st.slider(
            "Spending Score", min_value=1, max_value=100, value=50
        )

    if st.button("Predict Persona", type="primary"):
        st.info(
            "The interface is ready. We need to connect these inputs "
            "to your model's exact prediction function and required features."
        )

elif page == "About":
    st.header("About the Project")
    st.write(
        "A customer analytics system that uses machine learning "
        "to group customers into meaningful personas."
    )
