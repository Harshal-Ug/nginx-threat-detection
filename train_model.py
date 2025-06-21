import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
df = pd.read_csv("features.csv")
numeric_df = df.select_dtypes(include='number')

model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)

model.fit(numeric_df)

df['anomaly_score'] = model.decision_function(numeric_df)
df['is_anomaly'] = model.predict(numeric_df)

print(df[['anomaly_score','is_anomaly']].head())

joblib.dump(model, "model.pkl")
