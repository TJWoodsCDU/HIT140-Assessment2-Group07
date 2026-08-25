import re
import pandas as pd

def load_data(path):
    return pd.read_csv(path, encoding="latin-1")

def extract_country_code(club_value):
    if pd.isna(club_value):
        return None
    match = re.match(r"^\d+\.([a-zA-Z]+)\s", club_value)
    return match.group(1) if match else None

EUROPE_CODES = {
    "eng", "sct", "es", "fr", "de", "it", "nl", "pt", "be", "at", "ch", "dk", "no", "se", "pl", "cz", "sk", "hu", "ro", "hr", "si", "rs", "bg", "gr", "ie", "tr", "ru", "kz", "cy", "il"
}

def classify_continent(country_code):
    if pd.isna(country_code):
        return "Unknown"
    return "Europe" if country_code in EUROPE_CODES else "Non-Europe"

def main(input_path, output_path):
    df =load_data(input_path)
    df["ClubCountryCode"] = df["Club"].apply(extract_country_code)
    df["ClubContinent"] = df["ClubCountryCode"].apply(classify_continent)

    all_codes = set(df["ClubCountryCode"].dropna().unique())
    unmapped = all_codes - EUROPE_CODES
    print("Country codes found:", sorted(all_codes))
    print()

    print("Classification summary:")
    print(df["ClubContinent"].value_counts())
    print()

    unknown_players = df[df["ClubContinent"] == "Unknown"]
    if len(unknown_players) > 0:
        print(f"{len(unknown_players)} player(s) with no club listed:")
        print(unknown_players[["Player"]].to_string(index=False))

    df.to_csv(output_path, index=False)
    print(f"\nSaved classified data to: {output_path}")
    return df

if __name__ == "__main__":
    main("data.csv", "classified_clubs.csv")
