#Inferential STATS
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
