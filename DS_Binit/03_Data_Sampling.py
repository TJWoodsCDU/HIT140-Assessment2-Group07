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
