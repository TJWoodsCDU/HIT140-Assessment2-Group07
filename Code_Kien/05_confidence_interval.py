import pandas as pd
import scipy.stats as st
import math

sample = pd.read_csv("Code_Kien/sample.csv", encoding="utf-8-sig")

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
