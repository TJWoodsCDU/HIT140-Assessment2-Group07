# 03_descriptive_stats.py
# Descriptive statistics and charts for SoT%, comparing Europe vs
# Non-Europe based players. Runs for both the population and the sample
# in one go now instead of having to flip INPUT_FILE and rerun twice.
import os
os.chdir(os.path.dirname(__file__))

import pandas as pd
import matplotlib.pyplot as plt

RUNS = [
    ("../datas/population.csv", True),   # (filename, is_population)
    ("../datas/sample.csv", False),
]

for INPUT_FILE, IS_POPULATION in RUNS:

    label = "population" if IS_POPULATION else "sample"
    print(f"\n=========== {label.upper()} RUN ===========")

    data = pd.read_csv(INPUT_FILE)

    europe = data[data["ClubContinent"] == "Europe"]["SoT%"]
    non_europe = data[data["ClubContinent"] == "Non-Europe"]["SoT%"]

    # ddof=0 means divide by N (population variance), ddof=1 means divide
    # by N-1 (sample variance). population.csv is the full population, so
    # ddof=0 there; sample.csv is an actual sample, so ddof=1.
    ddof = 0 if IS_POPULATION else 1

    for name, group in [("Europe", europe), ("Non-Europe", non_europe)]:
        print(f"\n{name} (n={len(group)})")
        print(f"  mean     = {group.mean():.2f}")
        print(f"  median   = {group.median():.2f}")
        print(f"  mode     = {group.mode()[0]:.2f}")
        print(f"  std dev  = {group.std(ddof=ddof):.2f}")
        print(f"  variance = {group.var(ddof=ddof):.2f}")
        print(f"  min/max  = {group.min():.1f} / {group.max():.1f}")
        print(f"  range    = {group.max() - group.min():.1f}")
        q1, q3 = group.quantile(0.25), group.quantile(0.75)
        print(f"  IQR      = {q3 - q1:.2f}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)
    ax1.hist(europe, bins=15, color="#2C5F2D", edgecolor="white")
    ax1.set_title("Europe")
    ax1.set_xlabel("Shot Accuracy (SoT%)")
    ax1.set_ylabel("Number of players")
    ax2.hist(non_europe, bins=15, color="#2C5F2D", edgecolor="white")
    ax2.set_title("Non-Europe")
    ax2.set_xlabel("Shot Accuracy (SoT%)")
    plt.tight_layout()
    plt.savefig(f"../datas/histogram_{label}.png", dpi=150)
    plt.close()

    # Boxplot -- easy way to see median, spread and any outliers at a glance.
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.boxplot([europe, non_europe], tick_labels=["Europe", "Non-Europe"])
    ax.set_ylabel("Shot Accuracy (SoT%)")
    plt.tight_layout()
    plt.savefig(f"../datas/boxplot_{label}.png", dpi=150)
    plt.close()

    print(f"\nSaved histogram_{label}.png and boxplot_{label}.png")