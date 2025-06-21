import pandas as pd
import json

df = pd.read_csv("nginx_logs.csv")
# print(df.head())

df['timestamp'] = pd.to_datetime(df['timestamp'],format = '%d/%b/%Y:%H:%M:%S %z')
df['hour_of_day'] = df['timestamp'].dt.hour
# print(df[['timestamp', 'hour_of_day']].head())

method_values = df['method'].unique()
# print(methods)
url_values= df['url'].unique()
# print(url_agents)
ua_values = df['user_agent'].unique()
# print(ua)
method_map= {}
for idx, value in enumerate(method_values):
    method_map [value] = idx
# print(method_map)

url_mapping = {val: idx for idx, val in enumerate(url_values)}
# print(url_mapping)
ua_mapping = {val: idx for idx, val in enumerate(ua_values)}
# print(ua_mapping)

df['method'] = df['method'].map(method_map)
df['url'] = df['url'].map(url_mapping)
df['user_agent'] = df['user_agent'].map(ua_mapping)
# print(df[['method', 'url', 'user_agent']].head())

encoder_dict = {
    "method": {"mapping": method_map},
    "path": {"mapping": url_mapping},
    "user_agent": {"mapping": ua_mapping}
}
with open("encoder_mapping.json", "w") as f:
   json.dump(encoder_dict,f,indent = 2)

print("Saved encoder mapping to json file")

df = df.drop(columns=['timestamp','http_version'])

df.to_csv("features.csv", index = False)
print("features.csv exported successfully")