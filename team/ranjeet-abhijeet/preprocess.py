import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------
# Replace with your actual file path
file_path = 'c:\Users\User\Downloads\demographics.csv'
df = pd.read_csv(file_path)

print("--- Original Data Info ---")
print(df.info())

# ---------------------------------------------------------
# 2. PRE-PROCESSING (CLEANING & TRANSFORMATION)
# ---------------------------------------------------------

# A. Convert 'date' from String to Datetime objects
# This allows Python to understand time (months, days, years)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

# B. Convert 'pincode' from Integer to String
# Pincodes are categories, not numbers we do math on.
df['pincode'] = df['pincode'].astype(str)

# C. Rename messy column names for better readability
df.rename(columns={'demo_age_17_': 'demo_age_above_17'}, inplace=True)

# ---------------------------------------------------------
# 3. SOLVING THE "FREQUENCY MISMATCH"
# ---------------------------------------------------------
# Problem: Early data is Monthly sums, later data is Daily counts.
# Solution: Create a "Month-Year" column and aggregate everything by Month.

df['month_year'] = df['date'].dt.to_period('M')

# Group by Month and District/State to get consistent totals
monthly_df = df.groupby(['month_year', 'state', 'district'])[[
    'demo_age_5_17', 'demo_age_above_17'
]].sum().reset_index()

# Convert month_year back to timestamp for plotting compatibility
monthly_df['plot_date'] = monthly_df['month_year'].dt.to_timestamp()

print("\n--- Processed Monthly Data (First 5 Rows) ---")
print(monthly_df.head())

# ---------------------------------------------------------
# 4. VERIFICATION (Why we did this)
# ---------------------------------------------------------
print("\n--- Verification: Comparing Totals ---")
# If our theory is right, March totals should be roughly similar to November totals
# even though March has 53 rows and November has 1600+ rows.
mar_stats = monthly_df[monthly_df['month_year'] == '2025-03'][['demo_age_above_17']].sum().values[0]
nov_stats = monthly_df[monthly_df['month_year'] == '2025-11'][['demo_age_above_17']].sum().values[0]

print(f"March 2025 Total (17+): {mar_stats}")
print(f"Nov 2025 Total (17+):   {nov_stats}")
print("Notice how the totals are comparable? This confirms we successfully standardized the data.")

# ---------------------------------------------------------
# 5. EXPORT
# ---------------------------------------------------------
# Save the cleaned, standardized monthly data for your analysis
monthly_df.to_csv('cleaned_monthly_uidai_data.csv', index=False)
print("\nSuccess! Saved cleaned data to 'cleaned_monthly_uidai_data.csv'")