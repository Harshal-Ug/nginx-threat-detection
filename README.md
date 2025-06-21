# 🔐 NGINX Security Threat Detection using Machine Learning

A lightweight system to detect security anomalies (like brute-force or DDoS attacks) from NGINX access logs using unsupervised machine learning.

![Demo](Demo_Video.mp4)
![streamlit manual_inspector]("screenshot/streamlit_output.png")


---

## 🚀 Overview

This project parses real-world NGINX access logs, extracts behavior-based features, and uses an Isolation Forest model to detect anomalies. It includes:

- Real-time log monitoring with alerts (notification + email)
- On-demand prediction via Streamlit UI
- Feature engineering + visualization
- Model training and result export

---

## 🧠 How It Works

1. **Log Parsing** – Raw NGINX logs are structured using regex and converted to a DataFrame.
2. **Feature Engineering** – Key attributes like request method, URL, user agent, status code, size, and request time are transformed and encoded.
3. **Anomaly Detection** – An unsupervised Isolation Forest model identifies rare behavior as potential threats.
4. **Real-Time Alerts** – If a log entry is flagged as anomalous, an email and desktop alert are triggered instantly.
5. **Streamlit Testing** – A separate UI allows you to simulate and test input patterns.
---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/Harshal-Ug/nginx-threat-detection.git
cd nginx-threat-detection

# Install dependencies
pip install -r requirements.txt

# Train the model (optional if model.pkl exists)
python train_model.py

## 🔐 Environment Variables Setup

To enable **real-time alerts and API predictions** in `watcher.py`, create a `.env` file inside the `watcher/` directory with the following keys:

```env
PREDICT_ONE_URL=http://127.0.0.1:8000/predict_one
NOGINX_MAIL_ID=your_email@gmail.com
NOGINX_MAIL_PASSWORD=your_email_app_password
RECEIVER_MAIL_ID=recipient_email@gmail.com
NGINX_LOG_PATH=nginx.log

# Start log watcher
python watcher/watcher.py

# Launch Streamlit app(manual inspection)
streamlit run streamlit_app/app.py
---

## ✅ Example: Real-Time Threat Detection

Here’s how a suspicious request is flagged in real-time by the watcher:

### 🔁 Sample Log Entry

203.0.113.101 - - [21/Jun/2025:20:01:01 +0000] "POST /admin.php HTTP/1.1" 404 142 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"
### 🧠 Encoded Payload Sent to Model

```json
{
  "status": 404,
  "size": 0.0004,
  "method": 2,
  "path": 6,
  "user_agent": 138,
  "hour_of_day": 20
}

### Output from watcher.py

📤 Sending payload: {...}
📥 API response: {"anomaly": true}
🚨 ALERT! Anomalous request detected!

