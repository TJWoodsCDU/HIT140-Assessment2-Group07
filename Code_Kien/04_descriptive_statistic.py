import pandas as pd

sample = pd.read_csv("Code_Kien/sample.csv", encoding="utf-8-sig")

# Measures of Central Tendency
mean_val = sample["MinPerMatch"].mean()
median_val = sample["MinPerMatch"].median()
mode_val = sample["MinPerMatch"].mode()

# Measures of Dispersion
range_val = sample["MinPerMatch"].max() - sample["MinPerMatch"].min()
iqr_val = sample["MinPerMatch"].quantile(0.75) - sample["MinPerMatch"].quantile(0.25)
variance_val = sample["MinPerMatch"].var()
std_val = sample["MinPerMatch"].std()

print(f"\nMean: {mean_val:.2f}")
print(f"Median: {median_val:.2f}")
print(f"Mode: {mode_val.tolist()}")

print(f"Range: {range_val:.2f}")
print(f"IQR: {iqr_val:.2f}")
print(f"Variance: {variance_val:.2f}")
print(f"Standard deviation: {std_val:.2f}")