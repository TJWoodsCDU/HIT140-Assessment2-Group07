import pandas as pd
import numpy as np
import scipy.stats as st
import math

# Data wrangling
print("\nData wrangling")

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

# Data preparation & sampling
print("\nData preparation & sampling")

population_size = len(df)
sample_size = 100
sample = df.sample(n=sample_size)

print(f"Sample size: {len(sample)} players")
print(sample[["Player", "Club", "MP", "Min", "MinPerMatch"]].head(10))

# Descriptive statistic
print("\nDescriptive statistic")

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

# Confidence interval
print("\nConfidence interval")

x_bar = sample["MinPerMatch"].mean()
s = sample["MinPerMatch"].std()
n = len(sample)

z_score = st.norm.ppf(q=0.975)

std_err = s / math.sqrt(n)

mrg_err = z_score * std_err

ci_low = x_bar - mrg_err
ci_upp = x_bar + mrg_err

print("Mean: %.2f. Standard deviation: %.2f. Size: %d." % (x_bar, s, n))
print("Z-statistic: %.2f" % z_score)
print("Standard error: %.2f" % std_err)
print("Margin of error: %.2f" % mrg_err)
print("Confidence Interval of the mean: %.2f to %.2f" % (ci_low, ci_upp))

# One-sample t-test
print("\nOne-sample t-test")

sample_data = sample["MinPerMatch"].to_numpy()

x_bar = st.tmean(sample_data)
s = st.tstd(sample_data)
print("\t Sample mean: %.2f" % x_bar)
print("\t Sample std. dev.: %.2f" % s)

t_stats, p_val = st.ttest_1samp(sample_data, threshold, alternative='less')
print("\n Computing t* ...")
print("\t t-statistic (t*): %.2f" % t_stats)

print("\n Computing p-value ...")
print("\t p-value: %.4f" % p_val)

print("\n Conclusion:")
if p_val < 0.05:
    print("\t We reject the null hypothesis.")
else:
    print("\t We accept the null hypothesis.")