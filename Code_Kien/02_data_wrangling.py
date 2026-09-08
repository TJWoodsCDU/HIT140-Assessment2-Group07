import pandas as pd
import numpy as np

df = pd.read_csv("Code_Kien/data.csv", encoding="latin1")
print("\nData raw shape:", df.shape)

cleaned_rows = []

for index, row in df.iterrows():

    if pd.isna(row['Min']) or pd.isna(row['MP']):
        continue

    if row['MP'] < 1:
        continue
        
    cleaned_rows.append(row)

df = pd.DataFrame(cleaned_rows)

df["MinPerMatch"] = df["Min"] / df["MP"]

# Capping player with MinPerMatch 90-minute threshold
threshhold = 90
df["MinPerMatch"] = np.where(
    df["MinPerMatch"] > threshhold,
    threshhold,
    df["MinPerMatch"]
)

print("\nPopulation size:", len(df))
print(df[["Player", "Club", "MP", "Min", "MinPerMatch"]].describe())

df.to_csv("Code_Kien/population_data.csv", index=False)
print("Saved: population_data.csv")