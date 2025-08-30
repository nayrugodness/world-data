# World Bank Data Downloader

This Python script downloads World Bank indicators for multiple countries and saves them in a **wide-format Excel file** ready for analysis and visualization.

## Features

* Fetches multiple indicators for multiple countries.
* Supports configurable start and end years.
* Generates a **single Excel sheet** with:

  * **Rows = years**
  * **Columns = indicator\_country** (e.g., `GDP_per_capita_USD_USA`)
* Fully configurable via `.env` file.

## Requirements

* Python 3.8+
* Packages:

```bash
pip install requests pandas tqdm python-dotenv openpyxl
```

## Setup

1. Clone or download the repository.
2. Create a `.env` file in the root folder based on `.env.example`. Example:

```env
COUNTRIES={"USA": "United States","COL": "Colombia","CAN": "Canada"}
INDICATORS={"NY.GDP.PCAP.CD":"GDP_per_capita_USD","SP.POP.TOTL":"Population_total","SP.POP.GROW":"Population_growth_pct","NV.AGR.TOTL.ZS":"Agriculture_value_added_pct_GDP","NE.EXP.GNFS.ZS":"Exports_pct_GDP","SP.RUR.TOTL.ZS":"Rural_population_pct","SE.SEC.ENRR":"School_enrollment_secondary_gross_pct","SP.DYN.LE00.IN":"Life_expectancy_years"}
START_YEAR=2004
END_YEAR=2024
PER_PAGE=2000
```

## Usage

Run the script:

```bash
python3 data.py
```

The script will fetch data from the World Bank API and save it in `wb_data_wide.xlsx` in the current directory.

## Configuration

The `.env` file allows you to easily modify:

* `COUNTRIES`: JSON dictionary of country codes to names.
* `INDICATORS`: JSON dictionary of World Bank indicator codes to readable names.
* `START_YEAR` and `END_YEAR`: Range of years for the data.
* `PER_PAGE`: Maximum number of rows to fetch per request.

## Output

`wb_data_wide.xlsx`:

* **Columns**: `{indicator}_{country_code}`
* **Rows**: Years

Example:

| year | GDP\_per\_capita\_USD\_USA | GDP\_per\_capita\_USD\_COL | Population\_total\_USA | … |
| ---- | -------------------------- | -------------------------- | ---------------------- | - |
| 2004 | 40000                      | 7000                       | 290000000              | … |
| 2005 | 41000                      | 7200                       | 292000000              | … |

## Notes

* The script respects minimal delay between API requests (`time.sleep(0.2)`).
* Handles missing data gracefully (empty cells in Excel for missing values).

## Guides

### 1. Country Codes Guide

This file (`country_codes.md`) contains the list of country codes and their corresponding country names so users can know which codes to use:

| Country Code | Country Name  |
| ------------ | ------------- |
| USA          | United States |
| COL          | Colombia      |
| CAN          | Canada        |
| ...          | ...           |

### 2. Indicator Codes Guide

This file (`indicator_codes.md`) contains the list of indicator codes and what they represent:

| Indicator Code | Description                             |
| -------------- | --------------------------------------- |
| NY.GDP.PCAP.CD | GDP per capita (USD)                    |
| SP.POP.TOTL    | Total Population                        |
| SP.POP.GROW    | Population Growth (%)                   |
| NV.AGR.TOTL.ZS | Agriculture value added (% of GDP)      |
| NE.EXP.GNFS.ZS | Exports (% of GDP)                      |
| SP.RUR.TOTL.ZS | Rural population (% of total)           |
| SE.SEC.ENRR    | School enrollment, secondary, gross (%) |
| SP.DYN.LE00.IN | Life expectancy at birth (years)        |

## License

MIT License

## Build by Nayru Alexandra Ramirez Molano, ChatGPT and Gemini IA