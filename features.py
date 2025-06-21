import pandas as pd
df = pd.read_csv("nginx_logs.csv")
# print(df.head())

df['timestamp'] = pd.to_datetime(df['timestamp'],format = '%d/%b/%Y:%H:%M:%S %z')
df['hour_of_day'] = df['timestamp'].dt.hour
print(df[['timestamp', 'hour_of_day']].head())
methods = df['method'].unique()
print(methods)