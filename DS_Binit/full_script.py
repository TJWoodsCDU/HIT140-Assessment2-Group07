	
# FIFA WORLD CUP 2026 - ANALYTICAL TASK - HIT140 FOUNDATIONS OF DATA SCIENCE
#
# Research Question:
#
# Is the average number of substitutions used by a team per match significantly different from the five-substitution benchmark?
#
# H0: μ = 5
#     The average number of substitutions per team per match is equal to 5.
#
# H1: μ ≠ 5
#     The average number of substitutions per team per match is different from 5.
#
# Significance level:
# α = 0.05
#
# Statistical test:
# Two-tailed one-sample t-test

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy import stats
from scipy.stats import ttest_1samp

df = pd.read_csv("fifa_playing_time.csv")
print("FIRST FIVE ROWS")
print(df.head()) 

print("\nCOLUMN LISTS")
print(df.columns.tolist())

print("\nDATA SHAPE")
print(df.shape)

print("\nDATA INFORMATION")
print(df.info())

print("\nNULL VALUES")
print(df.isnull().sum())


#DATA INFORMATION

analysis_df = df[
    ["Squad", "MP", "Min", "Subs"]
].copy()
analysis_df

## Removing the extra null value row
last_index = analysis_df.index[-1] # this will be 48
analysis_df = analysis_df.drop(last_index)
analysis_df = analysis_df.reset_index(drop = True) 
print(analysis_df.info())
print (analysis_df.isnull().sum())


##Calculate substitution per match played of each team

analysis_df["Subs_per_match"] = (analysis_df["Subs"] / analysis_df["MP"])
##Cleaned data
print("\nCLEANED DATA")
print(
    analysis_df[
        [
            "Squad",
            "MP",
            "Min",
            "Subs",
            "Subs_per_match"
        ]
    ]
)

##Check range of substitution per match
print("\nMinimum substitutions per match:")
print(
    analysis_df["Subs_per_match"].min()
)

print("\nMaximum substitutions per match:")
print(
    analysis_df["Subs_per_match"].max()
)

# DATA SAMPLING

# We randomly select 30 teams.
# random_state=42 ensures that the same sample is obtained every time the program is run.

sample_size = min(30, len(analysis_df))

sample = analysis_df.sample(
    n=sample_size,
    random_state=7
).copy()
#printing the random sample values
print("RANDOM SAMPLE")

print(
    sample[
        [
            "Squad",
            "MP",
            "Min",
            "Subs",
            "Subs_per_match"
        ]
    ].to_string(index=False)
)

print("\nSample size:",end="")
print(len(sample))

# Descriptive statistics
values = sample["Subs_per_match"]

sample_size = len(values)

mean_subs = values.mean()

median_subs = values.median()

std_subs = values.std(
    ddof=1
)

variance_subs = values.var(
    ddof=1
)

minimum_subs = values.min()

maximum_subs = values.max()

q1 = values.quantile(0.25)

q3 = values.quantile(0.75)
print("DESCRIPTIVE STATISTICS")

print(
    f"Sample size:              {sample_size}"
)

print(
    f"Mean:                     {mean_subs:.2f}"
)

print(
    f"Median:                   {median_subs:.2f}"
)

print(
    f"Standard deviation:       {std_subs:.2f}"
)

print(
    f"Variance:                 {variance_subs:.2f}"
)

print(
    f"Minimum:                  {minimum_subs:.2f}"
)

print(
    f"First quartile (Q1):      {q1:.2f}"
)

print(
    f"Third quartile (Q3):      {q3:.2f}"
)

print(
    f"Maximum:                  {maximum_subs:.2f}"
)

# 95% CONFIDENCE INTERVAL

# We use a t-distribution because the population standard deviation is unknown and we are estimating it from the sample.

confidence_level = 0.95

degrees_of_freedom = sample_size - 1

standard_error = (std_subs / np.sqrt(sample_size))

t_critical = stats.t.ppf((1 + confidence_level) / 2, degrees_of_freedom)

margin_of_error = (t_critical * standard_error)

lower_ci = (mean_subs - margin_of_error)

upper_ci = (mean_subs + margin_of_error)
#DISPLAY CONFIDENCE INTERVAL

print("\n95% CONFIDENCE INTERVAL")

print(
    f"Sample mean:             {mean_subs:.2f}"
)

print(
    f"Standard error:          {standard_error:.4f}"
)

print(
    f"t-critical value:        {t_critical:.4f}"
)

print(
    f"Margin of error:         {margin_of_error:.4f}"
)

print(
    f"Lower confidence limit:  {lower_ci:.2f}"
)

print(
    f"Upper confidence limit:  {upper_ci:.2f}"
)

print(
    f"\n95% CI: ({lower_ci:.2f}, {upper_ci:.2f})"
)

#ONE-SAMPLE T-TEST

# Benchmark:
# Five substitutions per team per match.

benchmark = 5


# Conduct a TWO-TAILED one-sample t-test.
#
# H0: μ = 5
# H1: μ ≠ 5

t_statistic, p_value = stats.ttest_1samp(values, popmean=benchmark)
# 23. DISPLAY T-TEST RESULTS

print("ONE-SAMPLE T-TEST")

print("Null hypothesis (H0): μ = 5")

print("Alternative hypothesis (H1): μ ≠ 5")

print("Test type: Two-tailed one-sample t-test")

print("Significance level: α = 0.05")

print(f"\nBenchmark mean: {benchmark:.2f}")

print(f"Sample mean:    {mean_subs:.2f}")

print(f"t-statistic:    {t_statistic:.4f}")

print(f"p-value:        {p_value:.4f}")


# STATISTICAL DECISION

alpha = 0.05

print("STATISTICAL DECISION")

if p_value < alpha:

    print("We reject the null hypothesis.")

    print(
        "There is statistically significant evidence that the average number of substitutions per team per match is different from five."
    )

else:

    print(
        "We fail to reject the null hypothesis."
    )

    print(
        "There is insufficient statistical evidence to conclude that the average number of substitutions per team per match is different from five."
    )

# HISTOGRAM

plt.figure(
    figsize=(10, 7)
)

counts, bins, patches = plt.hist(
    values,
    bins=8,
    edgecolor="black",
    alpha=0.7
)

# Add the frequency above each bar
for count, patch in zip(counts, patches):
    if count > 0:
        plt.text(
            patch.get_x() + patch.get_width() / 2,
            count,
            str(int(count)),
            ha="center",
            va="bottom"
        )

# Add benchmark line

plt.axvline(
    benchmark,
    color="red",
    linestyle="--",
    linewidth=2,
    label="Five-substitution benchmark"
)

# Add sample mean line

plt.axvline(
    mean_subs,
    color="blue",
    linestyle="-",
    linewidth=2,
    label=f"Sample mean = {mean_subs:.2f}"
)

plt.xlabel(
    "Substitutions per team per match"
)

plt.ylabel(
    "Number of teams"
)

plt.title(
    "Distribution of Substitutions per Team per Match"
)

plt.legend()

plt.tight_layout()

plt.show()

# HEATMAP

import seaborn as sns 

heatmap_data = sample[
    ["Squad", "Subs_per_match"]
].copy()

heatmap_data = heatmap_data.sort_values(
    "Subs_per_match"
)

heatmap_data = heatmap_data.set_index(
    "Squad"
)

plt.figure(figsize=(6, 10))

sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".2f",
    cmap="YlOrRd",
    linewidths=0.5,
    cbar_kws={
        "label": "Substitutions per match"
    }
)

plt.title(
    "Substitutions per Match by Team"
)

plt.xlabel("")
plt.ylabel("Team")

plt.tight_layout()
plt.show()

# FINAL SUMMARY

print("FINAL SUMMARY")

print(
    f"Question: Is the average number of substitutions used by a team per match significantly different from five?"
)

print(
    f"\nSample size: {sample_size}"
)

print(
    f"Sample mean: {mean_subs:.2f} substitutions/match"
)

print(
    f"95% confidence interval: "
    f"({lower_ci:.2f}, {upper_ci:.2f})"
)

print(
    f"t-statistic: {t_statistic:.4f}"
)

print(
    f"p-value: {p_value:.4f}"
)

if p_value < alpha:

    print(
        "\nFINAL CONCLUSION:"
    )

    print(
        "Reject H0. The average number of substitutions per team per match is statistically significantly different from five."
    )

else:

    print(
        "\nFINAL CONCLUSION:"
    )

    print(
        "Fail to reject H0. There is insufficient evidence to conclude that the average number of substitutions per team per match is significantly different from five."
    )

print("\nAnalysis complete.")
