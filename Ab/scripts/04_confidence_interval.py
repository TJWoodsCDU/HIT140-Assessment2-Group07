# 04_confidence_interval.py
# 95% confidence interval for the mean SoT% in each group, and for the
# difference between the two groups. Run once for the population, once for the sample.


import pandas as pd
import math

INPUT_FILE = "population.csv"   # change to "sample.csv" for the sample run

# t-critical values for a 95% CI, looked up from a t-table.
# Population run: Europe df=274, Non-Europe df=71, difference df=345
# Sample run:     Europe df=59,  Non-Europe df=59, difference df=118
if INPUT_FILE == "population.csv":
    T_EUROPE = 1.969
    T_NON_EUROPE = 1.994
    T_DIFFERENCE = 1.967
else:
    T_EUROPE = 2.001
    T_NON_EUROPE = 2.001
    T_DIFFERENCE = 1.980

data = pd.read_csv(INPUT_FILE)
europe = data[data["ClubContinent"] == "Europe"]["SoT%"]
non_europe = data[data["ClubContinent"] == "Non-Europe"]["SoT%"]

# --- CI for each group's mean ---
for name, group, t_crit in [("Europe", europe, T_EUROPE), ("Non-Europe", non_europe, T_NON_EUROPE)]:
    n = len(group)
    mean = group.mean()
    se = group.std(ddof=1) / math.sqrt(n)   # standard error
    lower = mean - t_crit * se
    upper = mean + t_crit * se
    print(f"{name}: mean={mean:.2f}, 95% CI = [{lower:.2f}, {upper:.2f}]")

# --- CI for the difference between the two group means ---
# Pooled variance assumes both groups have the same underlying variance.
n1, n2 = len(europe), len(non_europe)
var1, var2 = europe.var(ddof=1), non_europe.var(ddof=1)
df = n1 + n2 - 2
pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / df
se_diff = math.sqrt(pooled_var * (1 / n1 + 1 / n2))
mean_diff = europe.mean() - non_europe.mean()

lower = mean_diff - T_DIFFERENCE * se_diff
upper = mean_diff + T_DIFFERENCE * se_diff

print(f"\nDifference in means (Europe - Non-Europe): {mean_diff:.2f}")
print(f"95% CI for the difference: [{lower:.2f}, {upper:.2f}]")

if lower <= 0 <= upper:
    print("0 is inside this interval -> 'no real difference' is plausible.")
else:
    print("0 is outside this interval -> a real difference looks likely.")


import matplotlib.pyplot as plt

means = [europe.mean(), non_europe.mean()]
errors = []
for group, t_crit in [(europe, T_EUROPE), (non_europe, T_NON_EUROPE)]:
    se = group.std(ddof=1) / math.sqrt(len(group))
    errors.append(t_crit * se)

fig, ax = plt.subplots(figsize=(6, 5))
ax.bar(["Europe", "Non-Europe"], means, yerr=errors, capsize=8,
       color=["#1B4332", "#D4AF37"], edgecolor="black", width=0.5)
ax.set_ylabel("Mean Shot Accuracy (SoT%)")
ax.set_title("Mean SoT% with 95% Confidence Interval")
for i, m in enumerate(means):
    ax.text(i, m + errors[i] + 1, f"{m:.1f}%", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig("bar_with_ci.png", dpi=150)
plt.close()
print("\nSaved bar_with_ci.png")
