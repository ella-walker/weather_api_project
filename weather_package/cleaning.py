import pandas as pd
import numpy as np
import re
import requests


# -----------------------------
# Scraping Function
# -----------------------------
def fetch_raw_table(url: str, email: str) -> pd.DataFrame:
    """
    Scrapes the Wikipedia ski resort comparison table.
    Returns the raw, uncleaned DataFrame.
    """
    ua = f"STAT386-class-scraper/1.0 (+{email})"

    r = requests.get(url, headers={"User-Agent": ua}, timeout=15)
    r.raise_for_status()

    tables = pd.read_html(r.text)
    return tables[4]  # the ski resort table


# -----------------------------
# Cleaning Helpers
# -----------------------------
def remove_brackets(text):
    """
    Removes bracketed references like [3] from strings.
    """
    if pd.isna(text):
        return text
    return re.sub(r"\[.*?\]", "", str(text)).strip()


def clean_numeric(val):
    """
    Removes non-numeric characters and converts to float.
    """
    if pd.isna(val):
        return np.nan
    val = re.sub(r"[^\d.]", "", str(val))
    return float(val) if val else np.nan


def convert_numeric_columns(df: pd.DataFrame, numeric_cols: list) -> pd.DataFrame:
    """
    Converts each column in numeric_cols to float using clean_numeric().
    """
    for col in numeric_cols:
        df[col] = df[col].apply(clean_numeric)
    return df


# -----------------------------
# MAIN CLEANING PIPELINE
# -----------------------------
def run_cleaning_pipeline(url: str, email: str) -> pd.DataFrame:
    """
    Runs the entire data cleaning pipeline:
    1. Scrapes the Wikipedia page
    2. Drops unneeded columns
    3. Renames columns
    4. Removes missing snowfall rows
    5. Cleans string/text columns
    6. Converts numeric columns
    Returns a cleaned DataFrame.
    """

    print("Running cleaning pipeline...")

    # Step 1: Scrape raw data
    df = fetch_raw_table(url, email)

    # Step 2: Remove last column (citations)
    df = df.iloc[:, :-1]

    # Step 3: Rename columns
    df.columns = [
        "Resort Name", "Nearest City", "State/Province",
        "Peak Elevation (ft)", "Base Elevation (ft)",
        "Vertical Drop (ft)", "Skiable Area (acres)",
        "Total Trails", "Total Lifts",
        "Average Annual Snowfall (inches)"
    ]

    # Step 4: Remove rows with missing snowfall
    df = df[df["Average Annual Snowfall (inches)"].notna()]

    # Step 5: Clean all string columns (remove brackets + trim spaces)
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].apply(remove_brackets).str.strip()

    # Step 6: Convert numeric columns to floats
    numeric_cols = [
        "Peak Elevation (ft)", "Base Elevation (ft)",
        "Vertical Drop (ft)", "Skiable Area (acres)",
        "Total Trails", "Total Lifts",
        "Average Annual Snowfall (inches)"
    ]
    df = convert_numeric_columns(df, numeric_cols)

    print("Cleaning complete.")
    return df

