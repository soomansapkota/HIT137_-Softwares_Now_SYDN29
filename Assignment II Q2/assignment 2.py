"""
Australian Temperature Analysis (Recursive Version with Comments)
-----------------------------------------------------------------
This program processes ALL .csv files under the "temperatures" folder.
Each CSV represents yearly data from multiple weather stations.

Functions:
  1. Seasonal averages across ALL stations & years
  2. Station(s) with the largest temperature range
  3. Most stable & most variable stations (by standard deviation)

Outputs (saved in text files):
  - average_temp.txt
  - largest_temp_range_station.txt
  - temperature_stability_stations.txt
"""

import os
import pandas as pd
import numpy as np

# Config
# Folder containing CSV files
DATA_DIR = "temperatures"

# Expected columns
BASE_COLUMNS = ["STATION_NAME", "STN_ID", "LAT", "LON"]
MONTH_COLUMNS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Map months to Australian seasons
MONTH_TO_SEASON = {
    "December": "Summer", "January": "Summer", "February": "Summer",
    "March": "Autumn", "April": "Autumn", "May": "Autumn",
    "June": "Winter", "July": "Winter", "August": "Winter",
    "September": "Spring", "October": "Spring", "November": "Spring",
}
SEASON_ORDER = ["Summer", "Autumn", "Winter", "Spring"]

# Output file names
OUT_AVG = "average_temp.txt"
OUT_RANGE = "largest_temp_range_station.txt"
OUT_STABILITY = "temperature_stability_stations.txt"


# Format and Clean
def format_temp(val: float) -> str:
    """Format temperature with 2 decimal places. Show 'N/A' if value is NaN."""
    if np.isnan(val):
        return "N/A"
    return f"{val:.2f}°C"

def clean_numeric(series: pd.Series) -> pd.Series:
    """Remove non-numeric symbols and convert to float. Invalid entries become NaN."""
    series = series.astype(str).str.replace(r"[^0-9.\-]", "", regex=True)
    return pd.to_numeric(series, errors="coerce")


# Recursive Functions
def find_csv_files(folder: str) -> list:
    """Recursively find all CSV files in a folder and its subfolders."""
    files = []
    try:
        for entry in os.listdir(folder):
            path = os.path.join(folder, entry)
            if os.path.isdir(path):
                files.extend(find_csv_files(path))
            elif entry.lower().endswith(".csv"):
                files.append(path)
    except Exception as e:
        print(f"Error accessing {folder}: {e}")
    return files


