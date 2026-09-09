# Descriptive statistics
values = sample["Subs_per_match"]

sample_size = len(values)

mean_subs = values.mean()

median_subs = values.median()

std_subs = values.std(
    ddof=1
)

variance_subs = values.var(
    ddof=1
)

minimum_subs = values.min()

maximum_subs = values.max()

q1 = values.quantile(0.25)

q3 = values.quantile(0.75)
print("DESCRIPTIVE STATISTICS")

print(
    f"Sample size:              {sample_size}"
)

print(
    f"Mean:                     {mean_subs:.2f}"
)

print(
    f"Median:                   {median_subs:.2f}"
)

print(
    f"Standard deviation:       {std_subs:.2f}"
)

print(
    f"Variance:                 {variance_subs:.2f}"
)

print(
    f"Minimum:                  {minimum_subs:.2f}"
)

print(
    f"First quartile (Q1):      {q1:.2f}"
)

print(
    f"Third quartile (Q3):      {q3:.2f}"
)

print(
    f"Maximum:                  {maximum_subs:.2f}"
)
