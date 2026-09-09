# 01_data_wrangling.py
# Loads the shooting stats + club data, works out which continent each
# player's club is in, and saves the result.
import os
os.chdir(os.path.dirname(__file__))

import pandas as pd

data = pd.read_csv("../datas/data.csv", encoding="latin1")


country_codes = []
for club in data["Club"]:
    if pd.isna(club):
        country_codes.append(None)
    else:
        after_dot = club.split(".")[1]     
        code = after_dot.split(" ")[0]     
        country_codes.append(code)

data["ClubCountryCode"] = country_codes

# 3 players had no club listed in the original FBref export. I looked them up manually instead of just dropping them or guessing:
# All three are non-European, so we fill in their country codes by hand.
data.loc[data["Player"] == "Abdulelah Al-Amri", "ClubCountryCode"] = "sa"
data.loc[data["Player"].str.contains("niyev", na=False), "ClubCountryCode"] = "ae"
data.loc[data["Player"] == "Mohanad Lasheen", "ClubCountryCode"] = "eg"


europe_codes = ["eng", "sct", "es", "fr", "de", "it", "nl", "pt", "be",
                 "at", "ch", "dk", "no", "se", "pl", "cz", "sk", "hu",
                 "ro", "hr", "si", "rs", "bg", "gr", "ie", "tr", "ru",
                 "kz", "cy", "il"]

continents = []
for code in data["ClubCountryCode"]:
    if pd.isna(code):
        continents.append("Unknown")
    elif code in europe_codes:
        continents.append("Europe")
    else:
        continents.append("Non-Europe")

data["ClubContinent"] = continents

print(data["ClubContinent"].value_counts())

data.to_csv("../datas/classified_clubs.csv", index=False)
print("\nSaved to classified_clubs.csv")
