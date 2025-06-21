# streamlit_app/app.py
import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load("../model.pkl")

# Title
st.title("🔍 NGINX Anomaly Detection")

# User input
st.header("Enter Request Features")

status = st.number_input("HTTP Status Code", min_value=100, max_value=599, value=200)
size = st.number_input("Response Size", min_value=0, value=512)
method = st.selectbox("Method (Encoded)", options=[-1, 0, 1, 2, 3], format_func=lambda x: f"{x} (unknown)" if x == -1 else str(x))
path = st.selectbox("Path (Encoded)", options=[-1] + list(range(10)), format_func=lambda x: f"{x} (unknown)" if x == -1 else str(x))
user_agent = st.selectbox("User Agent (Encoded)", options=[-1] + list(range(150)), format_func=lambda x: f"{x} (unknown)" if x == -1 else str(x))
hour = st.slider("Hour of Day", 0, 23, 12)



# Predict button
if st.button("Predict"):
    features = np.array([[status, size, method, path, user_agent, hour]])
    prediction = model.predict(features)[0]
    is_anomaly = prediction == -1

    if is_anomaly:
        st.error("🚨 Anomaly Detected!")
    else:
        st.success("✅ Normal Request")

