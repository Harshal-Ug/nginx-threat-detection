import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("features.csv")

plt.figure(figsize=(6,4))
sns.countplot(x='status', data = df)
plt.title("Status Code Distribution")
plt.xlabel("HTTP Status")
plt.ylabel("count")
plt.tight_layout()
plt.show()

plt.figure(figsize=(6,4))
sns.histplot(df['size'], bins = 30 , kde = True)
plt.title("Response Size Distrubution")
plt.xlabel("Size(bytes)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

plt.figure(figsize=(6, 4))
sns.countplot(x='hour_of_day', data=df, hue='hour_of_day', palette='coolwarm', legend=False)
plt.title("Requests by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Requests")
plt.tight_layout()
plt.show()

plt.figure(figsize=(6, 4))
sns.countplot(x='method', data=df)
plt.title("HTTP Method Distribution")
plt.xlabel("Method (encoded)")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
numeric_df = df.select_dtypes(include='number')
sns.heatmap(numeric_df.corr(), annot=True, cmap="YlGnBu", fmt=".2f")
plt.title("Feature Correlation Heatmap")
plt.tight_layout()
plt.show()
