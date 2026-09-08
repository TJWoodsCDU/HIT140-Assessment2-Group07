# Club Continent & Shot Accuracy: Task Write-Up

**Analytic question:** Is there a significant difference in shot accuracy
(SoT%) between FIFA World Cup 2026 players based at European clubs and
players based at non-European clubs?

**Variables and level of measurement:**

| Variable | Level | Type |
|---|---|---|
| `SoT%` (shot accuracy) | Ratio | Continuous |
| `Sh`, `SoT` (shots, shots on target) | Ratio | Discrete |
| `ClubContinent` (Europe / Non-Europe) | Nominal | Categorical |
| `Club` | Nominal | Categorical |

---

## 1. Data Wrangling

- **Source:** FBref Shooting Stats table, FIFA World Cup 2026
  (`fbref.com/en/comps/1/shooting/World-Cup-Stats`) all 1,039 players who
  featured in the tournament.
- **Join:** club affiliation was pulled from a second FBref export (Standard
  Stats table, which includes a `Club` field) and combined with the shooting
  data using a **left join** on a shared row key, keeping every row from the
  shooting table and attaching the matching `Club` value from the second
  table.
- **Missing data — listwise deletion:** SoT% is undefined for any player
  with zero shots, and unreliable for very low shot counts (e.g. 1 shot on
  target out of 1 attempt reads as a "perfect" 100%). Players with fewer
  than 3 shots were excluded row-wise (listwise/case deletion).
- **3 players had no club listed** in the export. Rather than drop them or
  guess, each was looked up manually and their club filled in by hand:
  Abdulelah Al-Amri (Al-Nassr FC, Saudi Arabia), Aziz Gʻaniyev (Al Bataeh
  CSC, UAE), and Mohanad Lasheen (Pyramids FC, Egypt) all non-European.
  Of the three, only Al-Amri had enough shots (4) to clear the 3-shot
  threshold below, so he's the only one of the three who ends up in the
  final population; the other two are excluded by the shot-count rule
  regardless, not because their club was unknown.
- **Feature engineering:** two new variables were engineered from the raw
  `Club` text field: `ClubCountryCode` (extracted by splitting the text) and
  `ClubContinent` (the classification derived from it) neither existed in
  the source data.
- **Encoding:** the raw export required `latin1` decoding rather than UTF-8
  due to how the file was saved during export; this affects the display of
  some accented player names only and has no effect on any numeric field
  used in the analysis.

## 2. Classifying Club Continent

`Club` values follow the pattern `"<tier>.<country code> <club name>"` (e.g.
`"1.eng Leeds United"`). The country code was extracted with basic string
splitting, then classified as **Europe** or **Non-Europe** using UEFA
membership (football convention) rather than strict geography, meaning
Turkey, Russia, Kazakhstan, Cyprus, and Israel are classified as Europe,
since their clubs compete in UEFA competitions. This classification was
independently verified against FBref's own country/confederation index
(`fbref.com/en/countries/`), which confirmed all 61 country codes present in
the data, including every transcontinental edge case.

## 3. Population vs. Sample

- **Population:** all 347 players meeting the shot-count and known-club
  criteria (275 Europe-based, 72 Non-Europe-based). This is a real,
  fully-observed population, not an estimate of a larger one.
- **Sample:** 60 players drawn from each group (120 total), using a fixed
  random seed (42) for reproducibility, to run the same analysis a second
  time as a robustness check on a smaller subset.
- Descriptive statistics are calculated accordingly: **population variance**
  (divides by N) for the 347-player population, and **sample variance**
  (divides by N−1) for the 120-player sample parameters describe the
  population; statistics estimate it from a sample.

## 4. Descriptive Statistics

| | n | Mean | Median | Mode | Std Dev | Variance | Min | Max | Range | IQR |
|---|---|---|---|---|---|---|---|---|---|---|
| **Europe (population)** | 275 | 34.52 | 33.3 | 0.0 | 22.93 | 525.97 (pop.) | 0.0 | 100.0 | 100.0 | 30.00 |
| **Non-Europe (population)** | 72 | 31.67 | 33.3 | 0.0 | 21.82 | 475.99 (pop.) | 0.0 | 75.0 | 75.0 | 30.82 |
| **Europe (sample)** | 60 | 34.49 | 33.3 | 0.0 | 24.59 | 604.71 (sample) | 0.0 | 100.0 | 100.0 | 33.62 |
| **Non-Europe (sample)** | 60 | 33.97 | 33.3 | 33.3 | 22.20 | 492.62 (sample) | 0.0 | 75.0 | 75.0 | 30.00 |

Medians are effectively identical between groups in both the population and
the sample; the mean gap is small (under 3 percentage points in the
population, under 1 in the sample) relative to the spread within each group.

**Distribution shape:** a histogram of SoT% for each group (see
`histogram_population.png`) shows a right-skewed distribution for both
groups, not a normal distribution there's a concentration of players at
low accuracy (many players with 0% shots taken, none on target), tapering
off toward higher values. This is expected for a bounded percentage built
from small shot counts, and is the reason the **Central Limit Theorem**
matters here: even though individual player SoT% values aren't normally
distributed, the *sampling distribution of the group mean* approaches normal
as group size grows (n=275, 72, 60, 60 are all reasonably large), which is
what justifies using a t-based confidence interval and t-test on the group
means despite the skew in the raw data.

## 5. Confidence Interval

Since the population standard deviation is unknown, a **t-based** confidence
interval was used (not a z-based one) consistent with using the
t-distribution once the population SD has to be estimated from the sample
itself.

95% CI for the difference in means (Europe - Non-Europe), using pooled
variance (assumes equal population variance between groups, df = n1+n2−2):

- **Population:** 2.86 [-3.07, 8.78], df = 345
- **Sample:** 0.53 [-7.94, 9.00], df = 118

Both intervals contain zero, meaning "no true difference" is a statistically
plausible value in both cases.

## 6. Two-Sample t-Test

Following the standard 4-step hypothesis testing process:

1. **State the hypotheses.**
   H₀: mean SoT% is equal between Europe-based and Non Europe-based players
   H₁: mean SoT% is not equal between the two groups (two-tailed)
2. **Choose the test and significance level.** A two-sample independent
   t-test, α = 0.05, using pooled variance (df = n1+n2−2).
3. **Calculate the test statistic and p-value.**

   | | t-statistic | df | p-value |
   |---|---|---|---|
   | **Population (n=347)** | 0.947 | 345 | 0.3442 |
   | **Sample (60/60)** | 0.124 | 118 | 0.9019 |

4. **Make a decision.** Both p-values are well above α = 0.05.

## 7. Conclusion

**We fail to reject H₀.** There is no statistically significant difference in
shot accuracy between players based at European clubs and players based at
non-European clubs at the FIFA World Cup 2026. The result holds consistently
across both the full population and an independent stratified sample.

**Interpretive note:** this doesn't contradict the visible concentration of
elite attacking talent in Europe 17 of the tournament's top 20 shooters *by
volume* are Europe-based. But shot volume and shot accuracy are different
constructs: volume reflects playing time and tactical role, while accuracy is
a rate that isn't automatically inherited from a league's overall quality.

## 8. Limitations

- The Europe/Non-Europe classification relies on a UEFA-membership
  convention rather than strict geography a defensible but explicit
  modeling choice, documented above.
- The 3-shot minimum threshold is a judgment call; a different cutoff could
  shift the qualifying population slightly.
- A handful of player names display encoding artifacts from the export
  process; this is cosmetic only and does not affect any statistic used in
  this analysis, since `Player` is not used in any calculation.
- Sample sizes are unequal in the full population (275 vs. 72); this was
  addressed with a pooled-variance t-test plus a balanced stratified-sample
  robustness check, rather than ignored.
- SoT% is right-skewed at the individual level (see histogram); inference
  here relies on the Central Limit Theorem applying to the group means, not
  on individual values being normally distributed.
