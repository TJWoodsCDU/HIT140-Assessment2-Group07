# 05_hypothesis_test.py
# Two-sample t-test comparing mean SoT% between Europe-based and
# Non-Europe-based players. Runs for both population and sample in one go.
import os
os.chdir(os.path.dirname(__file__))

import pandas as pd
import math

ALPHA = 0.05
RUNS = ["../datas/population.csv", "../datas/sample.csv"]


def normal_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


for INPUT_FILE in RUNS:

    label = "population" if INPUT_FILE == "../datas/population.csv" else "sample"
    print(f"\n=========== {label.upper()} RUN ===========")

    data = pd.read_csv(INPUT_FILE)
    europe = data[data["ClubContinent"] == "Europe"]["SoT%"]
    non_europe = data[data["ClubContinent"] == "Non-Europe"]["SoT%"]

    n1, n2 = len(europe), len(non_europe)
    mean1, mean2 = europe.mean(), non_europe.mean()
    var1, var2 = europe.var(ddof=1), non_europe.var(ddof=1)

    df = n1 + n2 - 2
    pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / df
    se_diff = math.sqrt(pooled_var * (1 / n1 + 1 / n2))
    t_stat = (mean1 - mean2) / se_diff

    p_value = 2 * (1 - normal_cdf(abs(t_stat)))

    print(f"t-statistic = {t_stat:.3f}")
    print(f"df = {df}")
    print(f"p-value = {p_value:.4f}")

    if p_value < ALPHA:
        print(f"\np < {ALPHA}, so we reject H0.")
        print("There IS a significant difference in shot accuracy between the two groups.")
    else:
        print(f"\np >= {ALPHA}, so we fail to reject H0.")
        print("There is NO significant difference in shot accuracy between the two groups.")