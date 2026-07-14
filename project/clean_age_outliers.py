"""
clean_age_outliers.py — Remove rows with the spurious housing_median_age == 2018
sentinel from the raw NC Housing CSV. Confirmed as a data-mapping error, not a
real age — removed rather than "corrected" to 0.

Run:  python clean_age_outliers.py --data NC_Housing_Prices_2018_cleanedd.csv
"""

import argparse
import pandas as pd

KEEP_COLS = [
    "population", "households", "median_income", "median_house_value",
    "total_bedrooms", "latitude", "longitude", "housing_median_age",
]

def main(data_path, output_path):
    df = pd.read_csv(data_path, usecols=KEEP_COLS)
    print(f"Total rows loaded: {len(df)}")

    bad_age_mask = df["housing_median_age"] == 2018
    bad_count = bad_age_mask.sum()
    print(f"Rows with housing_median_age == 2018: {bad_count}")

    df_clean = df[~bad_age_mask]
    print(f"Rows remaining after removal: {len(df_clean)}")

    df_clean.to_csv(output_path, index=False)
    print(f"Saved cleaned file to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="NC_Housing_Prices_2018_cleanedd.csv")
    parser.add_argument("--output", default="NC_Housing_Prices_2018_age_cleaned.csv")
    args = parser.parse_args()
    main(args.data, args.output)