
import streamlit as st
import pandas as pd
from pathlib import Path
from predict_persona import predict_cluster

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Customer Persona Analytics",
    page_icon="🔐",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    file_path = BASE_DIR / "Mall_Customers.csv"
    if file_path.exists():
        return pd.read_csv(file_path)
    return None

df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔐 Persona Analytics")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Predict Persona", "Customer Data", "About"]
)

st.sidebar.caption("Machine Learning • Customer Insights")

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.title("📊 Customer Persona Analytics")
    st.write("Explore customer behaviour and discover customer segments.")

    if df is not None:
        c1, c2, c3 = st.columns(3)

        c1.metric("Total Customers", len(df))

        if "Age" in df.columns:
            c2.metric("Average Age", f"{df['Age'].mean():.1f} years")

        income_col = "Annual Income (k$)"
        if income_col in df.columns:
            c3.metric(
                "Average Annual Income",
                f"${df[income_col].mean():.1f}k"
            )

        st.divider()
        st.subheader("Customer Insights")

        left, right = st.columns(2)

        with left:
            if "Age" in df.columns:
                st.write("**Customer Age Distribution**")
                st.bar_chart(df["Age"].value_counts().sort_index())

        with right:
            score_col = "Spending Score (1-100)"
            if score_col in df.columns:
                st.write("**Spending Score Distribution**")
                st.bar_chart(
                    df[score_col].value_counts().sort_index()
                )

        if income_col in df.columns and score_col in df.columns:
            st.write("**Income vs Spending Score**")
            st.scatter_chart(
                df,
                x=income_col,
                y=score_col
            )

    else:
        st.warning(
            "Mall_Customers.csv was not found. "
            "Place it in the same folder as app.py."
        )

# ---------------- PREDICT PERSONA ----------------
elif page == "Predict Persona":
    st.title("🎯 Predict Customer Persona")
    st.write("Enter customer details to predict their K-means cluster.")

    with st.form("persona_form"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input(
                "Age", min_value=18, max_value=100, value=25
            )
            gender = st.selectbox(
                "Gender", ["Male", "Female"]
            )

        with col2:
            income = st.number_input(
                "Annual Income (k$)",
                min_value=0.0,
                max_value=1000.0,
                value=60.0,
                step=1.0
            )
            spending_score = st.slider(
                "Spending Score",
                min_value=1,
                max_value=100,
                value=75
            )

        submitted = st.form_submit_button(
            "Predict Persona", type="primary"
        )

    if submitted:
        try:
            cluster = predict_cluster(
                int(age),
                gender,
                float(income),
                float(spending_score)
            )

            st.success("Prediction completed successfully!")

            st.subheader("Prediction Result")
            st.metric("Predicted Cluster", f"Cluster {cluster}")

            st.info(
                "This is the cluster assigned by your trained "
                "K-means model. Its business meaning must be "
                "confirmed using the training data."
            )

            result = pd.DataFrame([{
                "Age": age,
                "Gender": gender,
                "Annual Income (k$)": income,
                "Spending Score (1-100)": spending_score,
                "Predicted Cluster": cluster
            }])

            st.dataframe(result, use_container_width=True)

            st.download_button(
                "Download Prediction",
                data=result.to_csv(index=False),
                file_name="persona_prediction.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Prediction failed: {e}")

# ---------------- CUSTOMER DATA ----------------
elif page == "Customer Data":
    st.title("👥 Customer Dataset")

    if df is not None:
        st.write("Explore the customer records used in this project.")
        st.dataframe(df, use_container_width=True)

        st.download_button(
            "Download Customer Data",
            data=df.to_csv(index=False),
            file_name="customer_data.csv",
            mime="text/csv"
        )
    else:
        st.error("Mall_Customers.csv was not found.")

# ---------------- ABOUT ----------------
elif page == "About":
    st.title("ℹ️ About the Project")

    st.markdown("""
    ### Secure Persona Prediction System

    This project uses machine learning to group customers
    according to their characteristics and spending behaviour.

    **Technologies**
    - Python
    - Streamlit
    - Pandas and NumPy
    - Scikit-learn
    - K-means clustering

    **Features**
    - Customer analytics dashboard
    - Customer persona prediction
    - Dataset exploration
    - Downloadable prediction results
    """)
