# 02_sampling.py
# Filters out players who barely shot at all, then defines our population
# and draws a stratified random sample from it.
import os
os.chdir(os.path.dirname(__file__))

import pandas as pd

data = pd.read_csv("../datas/classified_clubs.csv")


MIN_SHOTS = 3
population = data[(data["Sh"] >= MIN_SHOTS) & (data["ClubContinent"] != "Unknown")]

print(f"Population size: {len(population)} players")
print(population["ClubContinent"].value_counts())

population.to_csv("../datas/population.csv", index=False)


SAMPLE_SIZE = 60
SEED = 42  
europe_sample = population[population["ClubContinent"] == "Europe"].sample(
    n=SAMPLE_SIZE, random_state=SEED)
non_europe_sample = population[population["ClubContinent"] == "Non-Europe"].sample(
    n=SAMPLE_SIZE, random_state=SEED)

sample = pd.concat([europe_sample, non_europe_sample])

print(f"\nSample size: {len(sample)} players")
print(sample["ClubContinent"].value_counts())

sample.to_csv("../datas/sample.csv", index=False)
print("\nSaved population.csv and sample.csv")
