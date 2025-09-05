import os
import pandas as pd
import numpy as np

# ---------------- Config ---------------- #
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


# ---------------- Helper Functions ---------------- #
def format_temp(val: float) -> str:
    """Format temperature with 2 decimal places. Show 'N/A' if value is NaN."""
    if np.isnan(val):
        return "N/A"
    return f"{val:.2f}°C"

def clean_numeric(series: pd.Series) -> pd.Series:
    """Remove non-numeric symbols and convert to float. Invalid entries become NaN."""
    series = series.astype(str).str.replace(r"[^0-9.\-]", "", regex=True)
    return pd.to_numeric(series, errors="coerce")


# ---------------- Recursive Functions ---------------- #
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

def read_csv_list(files: list, idx: int = 0) -> list:
    """Recursively read all CSV files into a list of DataFrames."""
    if idx >= len(files):
        return []
    df = read_csv_file(files[idx])
    rest = read_csv_list(files, idx + 1)
    return ([df] if not df.empty else []) + rest

def merge_dataframes(dfs: list, idx: int = 0) -> pd.DataFrame:
    """Recursively merge a list of DataFrames into one."""
    if idx >= len(dfs):
        return pd.DataFrame()
    if idx == len(dfs) - 1:
        return dfs[idx]
    return pd.concat([dfs[idx], merge_dataframes(dfs, idx + 1)], ignore_index=True)

def mean_by_season(df: pd.DataFrame, order: list, col: str, idx: int = 0) -> dict:
    """Recursively compute the mean temperature for each season."""
    if idx >= len(order):
        return {}
    season = order[idx]
    vals = df.loc[df["Season"] == season, col].dropna()
    avg = float(vals.mean()) if not vals.empty else float("nan")
    rest = mean_by_season(df, order, col, idx + 1)
    rest[season] = avg
    return rest


# ---------------- Core Logic ---------------- #
def read_csv_file(path: str) -> pd.DataFrame:
    """Read a single CSV file safely, clean data, and return a DataFrame."""
    try:
        print(f"Reading: {path}")
        df = pd.read_csv(path)
        df.columns = [c.strip() for c in df.columns]  # Remove extra spaces

        # Ensure required columns exist
        missing = [c for c in (BASE_COLUMNS + MONTH_COLUMNS) if c not in df.columns]
        if missing:
            print(f"Skipping {path}, missing: {missing}")
            return pd.DataFrame()

        # Clean numeric columns (months)
        for m in MONTH_COLUMNS:
            df[m] = clean_numeric(df[m])

        print(f"Loaded {len(df)} rows")
        return df[BASE_COLUMNS + MONTH_COLUMNS]
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return pd.DataFrame()

def to_long_format(df: pd.DataFrame) -> pd.DataFrame:
    """Convert wide-format data (columns = months) into long format (Month, Temp)."""
    long_df = df.melt(
        id_vars=BASE_COLUMNS,
        value_vars=MONTH_COLUMNS,
        var_name="Month", value_name="Temp"
    )
    long_df["Season"] = long_df["Month"].map(MONTH_TO_SEASON)
    return long_df.dropna(subset=["Temp"])

def save_to_file(path: str, lines: list):
    """Save results to a text file."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"Wrote {path}")
    except Exception as e:
        print(f"Error writing {path}: {e}")

def calculate_seasonal_average(df: pd.DataFrame):
    """Calculate and save seasonal average temperatures."""
    print("Calculating seasonal averages...")
    means = mean_by_season(df, SEASON_ORDER, "Temp")
    lines = [f"{s}: {format_temp(means[s])}" for s in SEASON_ORDER]
    save_to_file(OUT_AVG, lines)

def calculate_temperature_range(df: pd.DataFrame):
    """Find station(s) with the largest temperature range."""
    print("Finding largest temp range...")
    per_station = df.groupby("STATION_NAME")["Temp"].agg(["min", "max"])
    per_station["Range"] = per_station["max"] - per_station["min"]
    max_r = per_station["Range"].max()
    ties = per_station[per_station["Range"] == max_r]
    lines = [
        f"{station}: Range {format_temp(row['Range'])} "
        f"(Max: {format_temp(row['max'])}, Min: {format_temp(row['min'])})"
        for station, row in ties.iterrows()
    ]
    save_to_file(OUT_RANGE, lines)

def calculate_stability(df: pd.DataFrame):
    """Find most stable (smallest std) and most variable (largest std) stations."""
    print("Calculating stability...")
    stds = df.groupby("STATION_NAME")["Temp"].std(ddof=0)
    min_std, max_std = stds.min(), stds.max()
    stable = stds[stds == min_std]
    variable = stds[stds == max_std]
    lines = []
    for st, v in stable.items():
        lines.append(f"Most Stable: {st}: StdDev {format_temp(v)}")
    for st, v in variable.items():
        lines.append(f"Most Variable: {st}: StdDev {format_temp(v)}")
    save_to_file(OUT_STABILITY, lines)


# Main Function
def main():
    """Main driver function to run the analysis."""
    print(f"Looking in: {DATA_DIR}")
    if not os.path.isdir(DATA_DIR):
        print(f"Folder not found: {DATA_DIR}")
        return

    # Find all CSV files
    files = find_csv_files(DATA_DIR)
    if not files:
        print("No CSV files found.")
        return
    print(f"Found {len(files)} CSV files")

    # Read CSVs into DataFrames
    dfs = read_csv_list(files)
    if not dfs:
        print("No valid data loaded.")
        return

    # Merge into one DataFrame
    print("Merging all CSVs...")
    df = merge_dataframes(dfs)
    print(f"Total rows: {len(df)}")

    # Convert to long format
    long_df = to_long_format(df)
    print(f"Long format rows: {len(long_df)}")

    # Perform calculations
    calculate_seasonal_average(long_df)
    calculate_temperature_range(long_df)
    calculate_stability(long_df)

    print("Analysis complete!")


if __name__ == "__main__":
    main()
