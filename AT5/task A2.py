
import pandas as pd

# Read the CSV file
df = pd.read_csv("Adyar.csv")

print("--- ORIGINAL DATA ---")
print(df)

# A2.1 – Cleaning Rules

# Convert columns into numeric values
df["pm25"] = pd.to_numeric(df["pm25"], errors="coerce")
df["temperature"] = pd.to_numeric(
    df["temperature"], errors="coerce"
)

# Remove impossible PM2.5 values
df.loc[
    (df["pm25"] < 0) | (df["pm25"] > 1000),
    "pm25"
] = pd.NA

# Remove duplicate readings
df = df.drop_duplicates(
    subset=["station_name", "date", "time"]
)

# Convert Fahrenheit into Celsius
mask = df["temp_unit"].str.upper() == "F"

df.loc[mask, "temperature"] = (
    df.loc[mask, "temperature"] - 32
) * 5 / 9

df.loc[mask, "temp_unit"] = "C"

# Sort records before filling missing values
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.sort_values(["station_name", "date", "time"])

# Fill missing PM2.5 using previous value
df["pm25"] = df.groupby("station_name")["pm25"].ffill()

# Fill remaining missing values using median
df["pm25"] = df["pm25"].fillna(df["pm25"].median())

# A2.2 – Normalisation

minimum = df["pm25"].min()
maximum = df["pm25"].max()

# Min-Max Normalisation
if maximum != minimum:
    df["pm25_minmax"] = (
        df["pm25"] - minimum
    ) / (maximum - minimum)
else:
    df["pm25_minmax"] = 0

# Z-Score Standardisation
mean = df["pm25"].mean()
std = df["pm25"].std()

if pd.notna(std) and std != 0:
    df["pm25_zscore"] = (
        df["pm25"] - mean
    ) / std
else:
    df["pm25_zscore"] = 0

# A2.3 – Standard Formatting

# Standard date format
df["date"] = df["date"].dt.strftime("%Y-%m-%d")

# Standard station names
df["station_name"] = (
    df["station_name"].str.strip().str.title()
)

# Standard number format
df["pm25"] = df["pm25"].round(2)
df["temperature"] = df["temperature"].round(2)

# Save cleaned data
df.to_csv("cleaned_air_quality.csv", index=False)

print("\n--- CLEANED DATA ---")
print(df)

print("\nCleaned data saved successfully")


# Alternative Concept – Dropping Missing Values

drop_df = df.dropna(subset=["pm25"])

print("\nRows after dropping missing values:", len(drop_df))

# Forward filling
forward_df = df.copy()
forward_df["pm25"] = forward_df["pm25"].ffill()

print("Rows after forward filling:", len(forward_df))

# Median filling
median_df = df.copy()
median_df["pm25"] = median_df["pm25"].fillna(
    median_df["pm25"].median()
)

print("Rows after median filling:", len(median_df))
