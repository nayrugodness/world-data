from dotenv import load_dotenv
import requests
import pandas as pd
from tqdm import tqdm
import time
import os
import json

# Load environment variables from .env file
load_dotenv()

# --------------------------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------------------------
COUNTRIES = json.loads(os.getenv("COUNTRIES"))  # Dictionary of country codes to names
INDICATORS = json.loads(os.getenv("INDICATORS"))  # Dictionary of World Bank indicators
START_YEAR = int(os.getenv("START_YEAR"))  # Start year for data
END_YEAR = int(os.getenv("END_YEAR"))  # End year for data
PER_PAGE = int(os.getenv("PER_PAGE"))  # Max rows per API request

# Base URL for World Bank API
WB_BASE = (
    "https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}"
    "?date={start}:{end}&format=json&per_page={per_page}"
)


def fetch_indicator(indicator, countries, start=START_YEAR, end=END_YEAR):
    """Fetch indicator data from the World Bank API for given countries and years.

    Args:
        indicator (str): World Bank indicator code (e.g., "NY.GDP.PCAP.CD").
        countries (list): List of country codes (e.g., ["USA", "COL"]).
        start (int): Start year.
        end (int): End year.

    Returns:
        pd.DataFrame: DataFrame with columns ['country', 'year', 'value'].
    """
    url = WB_BASE.format(
        countries=";".join(countries),
        indicator=indicator,
        start=start,
        end=end,
        per_page=PER_PAGE,
    )
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Return empty DataFrame if no data
    if len(data) < 2 or data[1] is None:
        return pd.DataFrame()

    rows = []
    for item in data[1]:
        rows.append({
            "country": item["country"]["id"],
            "year": int(item["date"]),
            "value": item["value"]
        })
    return pd.DataFrame(rows)


def build_wide_panel(countries_codes, indicators):
    """Build a wide-format DataFrame for multiple indicators and countries.

    Each column corresponds to one indicator-country combination.
    Rows are indexed by year.

    Args:
        countries_codes (dict): Mapping of country codes to names.
        indicators (dict): Mapping of indicator codes to readable names.

    Returns:
        pd.DataFrame: Merged wide-format DataFrame with all indicators.
    """
    all_dfs = {}

    for code, name in tqdm(indicators.items(), desc="Fetching indicators"):
        time.sleep(0.2)  # Avoid hitting API too fast
        df = fetch_indicator(code, list(countries_codes.keys()), START_YEAR, END_YEAR)

        if df.empty:
            print(f"⚠️ No data for indicator {code}")
            continue

        # Pivot table: rows = year, columns = country
        df_pivot = df.pivot_table(index="year", columns="country", values="value")

        # Rename columns to include indicator name
        df_pivot.columns = [f"{name}_{c}" for c in df_pivot.columns]
        all_dfs[name] = df_pivot

    # Merge all indicators into one DataFrame
    merged = None
    for df in all_dfs.values():
        merged = df if merged is None else merged.join(df, how="outer")

    return merged.sort_index() if merged is not None else pd.DataFrame()


def save_excel_wide(merged_df, filename="wb_data_wide.xlsx"):
    """Save the wide-format DataFrame to an Excel file.

    Args:
        merged_df (pd.DataFrame): DataFrame to save.
        filename (str): Path to Excel file.
    """
    merged_df.to_excel(filename)
    print(f"✅ Excel file saved: {filename}")


def main():
    """Main function to fetch data and save to Excel."""
    merged_df = build_wide_panel(COUNTRIES, INDICATORS)
    if merged_df.empty:
        print("⚠️ No data downloaded; check indicators or connectivity.")
        return
    save_excel_wide(merged_df)


if __name__ == "__main__":
    main()
