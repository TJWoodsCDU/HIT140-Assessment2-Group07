#Inferential Statistics
# 95% CONFIDENCE INTERVAL
# We use a t-distribution because the population standard deviation is unknown and we are estimating it from the sample.

confidence_level = 0.95

degrees_of_freedom = sample_size - 1

standard_error = (std_subs / np.sqrt(sample_size))

t_critical = stats.t.ppf((1 + confidence_level) / 2, degrees_of_freedom)

margin_of_error = (t_critical * standard_error)

lower_ci = (mean_subs - margin_of_error)

upper_ci = (mean_subs + margin_of_error)
#DISPLAY CONFIDENCE INTERVAL

print("\n95% CONFIDENCE INTERVAL")

print(
    f"Sample mean:             {mean_subs:.2f}"
)

print(
    f"Standard error:          {standard_error:.4f}"
)

print(
    f"t-critical value:        {t_critical:.4f}"
)

print(
    f"Margin of error:         {margin_of_error:.4f}"
)

print(
    f"Lower confidence limit:  {lower_ci:.2f}"
)

print(
    f"Upper confidence limit:  {upper_ci:.2f}"
)

print(
    f"\n95% CI: ({lower_ci:.2f}, {upper_ci:.2f})"
)
