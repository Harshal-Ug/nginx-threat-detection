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
method = st.selectbox("Method (Encoded)", options=[0, 1, 2, 3])
path = st.selectbox("Path (Encoded)", options=list(range(10)))  # Adjust based on your encoding
user_agent = st.selectbox("User Agent (Encoded)", options=list(range(10)))  # Same here
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

