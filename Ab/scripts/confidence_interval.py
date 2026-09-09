# 04_confidence_interval.py
# 95% confidence interval for the mean SoT% in each group, and for the
# difference between the two groups. Runs for both population and sample
# in one go now instead of having to flip INPUT_FILE and rerun twice.
import os
os.chdir(os.path.dirname(__file__))

import pandas as pd
import math
import matplotlib.pyplot as plt

# t-critical values for a 95% CI, looked up from a t-table.
# Population run: Europe df=274, Non-Europe df=71, difference df=345
# Sample run:     Europe df=59,  Non-Europe df=59, difference df=118
T_CRIT = {
    "../datas/population.csv": {"europe": 1.969, "non_europe": 1.994, "difference": 1.967},
    "../datas/sample.csv":      {"europe": 2.001, "non_europe": 2.001, "difference": 1.980},
}

RUNS = ["../datas/population.csv", "../datas/sample.csv"]

for INPUT_FILE in RUNS:

    label = "population" if INPUT_FILE == "../datas/population.csv" else "sample"
    print(f"\n=========== {label.upper()} RUN ===========")

    data = pd.read_csv(INPUT_FILE)
    europe = data[data["ClubContinent"] == "Europe"]["SoT%"]
    non_europe = data[data["ClubContinent"] == "Non-Europe"]["SoT%"]

    n1, n2 = len(europe), len(non_europe)

    t_europe = T_CRIT[INPUT_FILE]["europe"]
    t_non_europe = T_CRIT[INPUT_FILE]["non_europe"]
    t_difference = T_CRIT[INPUT_FILE]["difference"]

    # --- CI for each group's mean ---
    for name, group, t_crit in [("Europe", europe, t_europe),
                                 ("Non-Europe", non_europe, t_non_europe)]:
        n = len(group)
        mean = group.mean()
        se = group.std(ddof=1) / math.sqrt(n)   # standard error
        lower = mean - t_crit * se
        upper = mean + t_crit * se
        print(f"{name}: mean={mean:.2f}, 95% CI = [{lower:.2f}, {upper:.2f}]")

    # --- CI for the difference between the two group means ---
    # Pooled variance assumes both groups have the same underlying variance.
    var1, var2 = europe.var(ddof=1), non_europe.var(ddof=1)
    df = n1 + n2 - 2
    pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / df
    se_diff = math.sqrt(pooled_var * (1 / n1 + 1 / n2))
    mean_diff = europe.mean() - non_europe.mean()

    lower = mean_diff - t_difference * se_diff
    upper = mean_diff + t_difference * se_diff

    print(f"\nDifference in means (Europe - Non-Europe): {mean_diff:.2f}")
    print(f"95% CI for the difference: [{lower:.2f}, {upper:.2f}]")

    if lower <= 0 <= upper:
        print("0 is inside this interval -> 'no real difference' is plausible.")
    else:
        print("0 is outside this interval -> a real difference looks likely.")

    means = [europe.mean(), non_europe.mean()]
    errors = []
    for group, t_crit in [(europe, t_europe), (non_europe, t_non_europe)]:
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
    plt.savefig(f"../datas/bar_with_ci_{label}.png", dpi=150)
    plt.close()
    print(f"\nSaved bar_with_ci_{label}.png")