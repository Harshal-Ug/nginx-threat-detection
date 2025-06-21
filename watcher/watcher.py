import os
import re
import pandas as pd
from datetime import datetime
import json
import requests
from plyer import notification
import smtplib
from email.mime.text import MIMEText
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

predict_one_url = os.getenv('PREDICT_ONE_URL')
noginx_mail_id = os.getenv('NOGINX_MAIL_ID')
noginx_mail_password = os.getenv('NOGINX_MAIL_PASSWORD')
receiver_mail_id = os.getenv('RECEIVER_MAIL_ID')

# Set path to nginx.log for local testing
filename = os.getenv("NGINX_LOG_PATH", "nginx.log")

# Log line regex pattern
pattern = re.compile(
    r'(?P<ip>[^\s]+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<url>\S+) (?P<http_version>[^"]+)" (?P<status>\d{3}) (?P<size>\d+) ".*?" "(?P<user_agent>[^"]+)"'
)

def encode_with_fallback(value, mapping):
    if value not in mapping:
        new_id = max(mapping.values(), default=-1) + 1
        mapping[value] = new_id
        # Save back to file
        with open(encoding_path, 'w') as f:
            json.dump(encoder_mappings, f, indent=2)
    return mapping[value]

def send_alert(df, method, path, user_agent):
    ip = df['ip'].values[0]
    timestamp = df['timestamp'].values[0]
    method = method.values[0]
    path = path.values[0]
    user_agent = user_agent.values[0]

    message = (
        f"🚨 Anomaly Detected!\n\n"
        f"IP: {ip}\n"
        f"Time: {timestamp}\n"
        f"Method: {method}\n"
        f"Path: {path}\n"
        f"User Agent: {user_agent}"
    )

    # Desktop alert
    try:
        notification.notify(
            title="🚨 noginx - Anomaly Alert",
            message=message,
            app_name="noginx",
            timeout=10
        )
    except Exception as e:
        print(f"Desktop notification failed: {e}")

    # Email alert
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(noginx_mail_id, noginx_mail_password)
        msg = MIMEText(message, _charset="utf-8")
        msg['Subject'] = "🚨 noginx - Anomaly Detected"
        msg['From'] = noginx_mail_id
        msg['To'] = receiver_mail_id
        s.sendmail(noginx_mail_id, receiver_mail_id, msg.as_string())
        s.quit()
        print("✅ Email alert sent.")
    except Exception as e:
        print("❌ Email failed:", e)

# Load encoder mappings
encoding_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','encoder_mapping.json'))
with open(encoding_path, 'r') as f:
    encoder_mappings = json.load(f)

def follow(filename):
    """Robust tail -f with log rotation/replacement handling."""
    print(f"👀 Watching file: {filename}")
    f = None
    inode = None
    while True:
        try:
            if f is None:
                f = open(filename, 'r')
                f.seek(0, os.SEEK_END)
                inode = os.fstat(f.fileno()).st_ino
                print(f"Opened file {filename}, inode {inode}")
            line = f.readline()
            if not line:
                # Check for file replacement (inode change)
                try:
                    if os.stat(filename).st_ino != inode:
                        print("🔄 Log file replaced or rotated. Reopening...")
                        f.close()
                        f = open(filename, 'r')
                        f.seek(0, os.SEEK_END)
                        inode = os.fstat(f.fileno()).st_ino
                        print(f"Reopened file {filename}, new inode {inode}")
                except FileNotFoundError:
                    print("Log file not found. Waiting...")
                    time.sleep(1)
                    continue
                time.sleep(0.5)
                continue
            yield line
        except Exception as e:
            print(f"Error in follow(): {e}")
            if f:
                f.close()
            f = None
            time.sleep(1)

def main():
    print(f"Watcher running, monitoring: {filename}")
    for line in follow(filename):
        print(f"Read line: {line.strip()}")
        match = pattern.search(line)
        if not match:
            print(f"⚠️ Line did not match pattern: {line.strip()}")
            continue

        df = pd.DataFrame([match.groupdict()])
        df['hour_of_day'] = df['timestamp'].apply(lambda x: int(datetime.strptime(x.split()[0], "%d/%b/%Y:%H:%M:%S").hour))
        df['path'] = df['url'].apply(lambda x: x.split('?')[0])
        df['status'] = df['status'].astype(int)
        df['size'] = df['size'].astype(int)

        # Save original fields for alert
        cur_method = df['method']
        cur_path = df['path']
        cur_user_agent = df['user_agent']

        # Apply encodings
        df['method'] = df['method'].apply(lambda x: encode_with_fallback(x, encoder_mappings['method']['mapping']))
        df['path'] = df['path'].apply(lambda x: encode_with_fallback(x, encoder_mappings['path']['mapping']))
        df['user_agent'] = df['user_agent'].apply(lambda x: encode_with_fallback(x, encoder_mappings['user_agent']['mapping']))

        feature_df = df[['status', 'size', 'method', 'path', 'user_agent', 'hour_of_day']]
        payload = feature_df.iloc[0].to_dict()

        print("📤 Sending payload:", payload)

        try:
            res = requests.post(predict_one_url, json=payload)
            print("📥 API response:", res.text)
            is_anomaly = res.json().get("anomaly", False)

            if is_anomaly:
                print("🔥 Anomaly Detected!")
                send_alert(df, cur_method, cur_path, cur_user_agent)
            else:
                print("✅ Normal request.")
        except Exception as e:
            print("[!] Error during processing:", e)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Watcher stopped by user.")
