import pandas as pd

df = pd.read_csv("data/diabetes.csv")
df["Country"] = "India"
df.to_csv("data/diabetes.csv", index=False)
print(df.head())
