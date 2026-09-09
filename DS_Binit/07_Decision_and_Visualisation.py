# STATISTICAL DECISION

alpha = 0.05

print("STATISTICAL DECISION")

if p_value < alpha:

    print("We reject the null hypothesis.")

    print(
        "There is statistically significant evidence that the average number of substitutions per team per match is different from five."
    )

else:

    print(
        "We fail to reject the null hypothesis."
    )

    print(
        "There is insufficient statistical evidence to conclude that the average number of substitutions per team per match is different from five."
    )

# HISTOGRAM

plt.figure(
    figsize=(10, 7)
)

counts, bins, patches = plt.hist(
    values,
    bins=8,
    edgecolor="black",
    alpha=0.7
)

# Add the frequency above each bar
for count, patch in zip(counts, patches):
    if count > 0:
        plt.text(
            patch.get_x() + patch.get_width() / 2,
            count,
            str(int(count)),
            ha="center",
            va="bottom"
        )

# Add benchmark line

plt.axvline(
    benchmark,
    color="red",
    linestyle="--",
    linewidth=2,
    label="Five-substitution benchmark"
)

# Add sample mean line

plt.axvline(
    mean_subs,
    color="blue",
    linestyle="-",
    linewidth=2,
    label=f"Sample mean = {mean_subs:.2f}"
)

plt.xlabel(
    "Substitutions per team per match"
)

plt.ylabel(
    "Number of teams"
)

plt.title(
    "Distribution of Substitutions per Team per Match"
)

plt.legend()

plt.tight_layout()

plt.show()

# HEATMAP

import seaborn as sns 

heatmap_data = sample[
    ["Squad", "Subs_per_match"]
].copy()

heatmap_data = heatmap_data.sort_values(
    "Subs_per_match"
)

heatmap_data = heatmap_data.set_index(
    "Squad"
)

plt.figure(figsize=(6, 10))

sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".2f",
    cmap="YlOrRd",
    linewidths=0.5,
    cbar_kws={
        "label": "Substitutions per match"
    }
)

plt.title(
    "Substitutions per Match by Team"
)

plt.xlabel("")
plt.ylabel("Team")

plt.tight_layout()
plt.show()
