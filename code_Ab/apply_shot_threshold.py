import pandas as pd

MIN_SHOTS = 3

def apply_threshold(input_path, output_path, min_shots=MIN_SHOTS):
    df = pd.read_csv(input_path, encoding="latin-1")

    before = len(df)

    qualified = df[(df["Sh"] >= min_shots) & (df["ClubContinent"] != "Unknown")].copy()
    after = len(qualified)

    print(f"Before filtering: {before} players")
    print(f"After filtering (Sh >= {min_shots}, known club continent): {after} players")
    print()
    print("Group sizes in your qualified sample")
    print(qualified["ClubContinent"].value_counts())

    qualified.to_csv(output_path, index=False)
    print(f"\nSaved analysis-ready data to: {output_path}")
    return qualified 

if __name__ == "__main__":
    apply_threshold("classified_clubs.csv", "qualified_players.csv")
