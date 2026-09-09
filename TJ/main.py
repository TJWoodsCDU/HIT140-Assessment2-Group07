import numpy as np
import pandas as pd
import scipy.stats as st

# Analytic Question Formulation
# Question: Is there a significant difference in average team age between teams
# that advanced past the group stage and teams that did not?

# Data Wrangling
data = pd.read_csv("data.csv")

# Drop missing values if any exist
data_clean = data.dropna(subset=["Squad", "Age", "MP"]).copy()

# Teams playing MP > 3 advanced past the group stage
# while MP == 3 did not
data_clean["Advanced"] = data_clean["MP"] > 3

# Data Preparation and Sampling
# Target Population: All possible national teams in the FIFA World Cup.
# Sample: 48 participating teams partitioned into two independent groups.
advanced_teams = data_clean[data_clean["Advanced"] == True]["Age"]
group_teams = data_clean[data_clean["Advanced"] == False]["Age"]


# Descriptive Statistics
def summary_stats(series, name):
    return {
        "Group": name,
        "Count": len(series),
        "Mean": series.mean(),
        "Median": series.median(),
        "Std Dev": series.std(ddof=1),
        "Min": series.min(),
        "Max": series.max()
    }


desc_table = pd.DataFrame([
    summary_stats(advanced_teams, "Advanced"),
    summary_stats(group_teams, "Group Stage")
])

print("DESCRIPTIVE STATISTICS")
print(desc_table.to_string(index=False))


# Inferential Statistics: Confidence Intervals (95%)
def calculate_ci(series, confidence=0.95):
    # number of teams in this group
    n = len(series)
    # average age for this group
    mean = np.mean(series)
    # standard error from mean
    sem = st.sem(series)
    # confidence interval
    h = sem * st.t.ppf((1 + confidence) / 2., n - 1)
    return mean - h, mean + h


adv_ci_low, adv_ci_high = calculate_ci(advanced_teams)
grp_ci_low, grp_ci_high = calculate_ci(group_teams)

print("\n95% CONFIDENCE INTERVALS FOR MEAN AGE")
print(f"Advanced Teams: Mean = {advanced_teams.mean():.2f} years | 95% CI = [{adv_ci_low:.2f}, {adv_ci_high:.2f}]")
print(f"Group Stage Teams: Mean = {group_teams.mean():.2f} years | 95% CI = [{grp_ci_low:.2f}, {grp_ci_high:.2f}]")

# Inferential Statistics: Two-Sample Independent t-Test
# Null Hypothesis: mu_advanced == mu_eliminated
# Alternative Hypothesis: mu_advanced != mu_eliminated
t_stat, p_val = st.ttest_ind(advanced_teams, group_teams, equal_var=True)

print("\nTWO-SAMPLE INDEPENDENT T-TEST RESULTS")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_val:.4f} (< 0.05 target)")
print(f"Conclusion: {"Reject Null Hypothesis (Statistically Significant)" if p_val < 0.05 else "Fail to Reject Null Hypothesis (No Statistically Significant Difference)"}")
