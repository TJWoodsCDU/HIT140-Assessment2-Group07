import pandas as pd

df = pd.read_csv("Code_Kien/population_data.csv", encoding="latin1")

population_size = len(df)
sample_size = 100
sample = df.sample(n=sample_size)

print(f"Population size: {population_size}")
print(f"Sample size: {sample_size}")
print(sample[["Player", "Club", "MP", "Min", "MinPerMatch"]].head(10))

sample.to_csv("Code_Kien/sample.csv", index=False)
print("Saved: sample.csv")