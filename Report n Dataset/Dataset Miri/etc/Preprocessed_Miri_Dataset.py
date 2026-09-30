import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import warnings

# Suppress warnings that might clutter output
warnings.filterwarnings('ignore')

# ==========================================
# 1. DATA LOADING
# ==========================================
print("Loading dataset...")

print("Loading 2018-2024 dataset...")
# The 2018-2024 dataset has 2 header rows to skip
df_dict = pd.read_excel('kuching_2018-2024.xlsx', sheet_name=None, skiprows=2)
df = pd.concat(list(df_dict.values()), ignore_index=True)

# Rename columns
col_mapping = {
    'Station ID': 'Site_Id',
    'Station Location': 'Site_Location',
    'NO₂ (Hourly)': 'No2_hourly',
    'O₃ (Hourly)': 'O3_hourly',
    'CO (Hourly)': 'Co_hourly',
    'PM₁₀ (Hourly)': 'Pm10_hourly',
    'PM₂.₅ (Hourly)': 'Pm2.5_hourly'
}
df = df.rename(columns=col_mapping)
# Dates are in YYYY-MM-DD HH:MM:SS format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Keep only relevant columns
cols_to_keep = ['Site_Id', 'Site_Location', 'Date', 'No2_hourly', 'O3_hourly', 'Co_hourly', 'Pm10_hourly', 'Pm2.5_hourly']
# Add missing columns with NaN if they don't exist
for col in cols_to_keep:
    if col not in df.columns: df[col] = np.nan

df = df[cols_to_keep]

# ==========================================
# 2. PREPARING THE DATASET
# ==========================================
print("Filtering for Miri location...")

# Filter for Miri first
df_miri_all = df[df['Site_Location'].str.contains('Miri', case=False, na=False)].copy()

# Drop rows with invalid dates
df_miri_all = df_miri_all.dropna(subset=['Date'])

# Create a Year column for grouping into sheets
df_miri_all['Year'] = df_miri_all['Date'].dt.year

# Create a YearMonth column for grouping within sheets
df_miri_all['YearMonth'] = df_miri_all['Date'].dt.to_period('M')

# Define Features (X) and Target (y)
target_column = 'Pm10_hourly'
feature_columns = ['No2_hourly', 'O3_hourly', 'Co_hourly']

output_filename = 'Prepared_Miri_Dataset.xlsx'
print(f"Saving to Excel file: {output_filename}")

# Initialize ExcelWriter
with pd.ExcelWriter(output_filename) as writer:
    for year in sorted(df_miri_all['Year'].unique()):
        print(f"\n=== Processing Year {year} ===")
        
        # Filter for the specific year
        df_year = df_miri_all[df_miri_all['Year'] == year]
        
        final_rows = []
        unique_periods = df_year['YearMonth'].unique()
        
        for period in sorted(unique_periods):
            print(f"--- Processing {period} ---")
            
            # Filter dataset for the specific month
            df_miri = df_year[df_year['YearMonth'] == period].copy()
            
            # Drop Year, YearMonth, Site_Id, and Site_Location columns
            columns_to_drop = ['Year', 'YearMonth', 'Site_Id', 'Site_Location']
            df_miri = df_miri.drop(columns=columns_to_drop, errors='ignore')

            # Get the full month name (e.g., "January")
            month_name = period.strftime('%B')
            
            num_cols = len(df_miri.columns)
            
            # Add the month name row (padded with empty strings)
            month_row = [month_name] + [''] * (num_cols - 1)
            final_rows.append(month_row)
            
            # Add the header row
            header_row = list(df_miri.columns)
            final_rows.append(header_row)
            
            # Add the data rows
            final_rows.extend(df_miri.values.tolist())
            
            # Add an empty row for spacing between months
            final_rows.append([''] * num_cols)

        # Create a single dataframe from the collected rows for the year
        df_final = pd.DataFrame(final_rows)

        # Save to a sheet named after the year
        df_final.to_excel(writer, sheet_name=str(year), index=False, header=False)

print(f"\n--- Preparation Complete ---")
print(f"All data has been saved to separate sheets per year in '{output_filename}' with month headers.")
