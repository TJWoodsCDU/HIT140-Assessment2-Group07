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


DATA INFORMATION

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
