import pandas as pd
import scipy.stats as st

sample = pd.read_csv("Code_Kien/sample.csv", encoding="latin1")

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

files_to_remove = ["population_played.csv", "sample.csv"]