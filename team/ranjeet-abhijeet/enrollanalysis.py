import pandas as pd

# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------
# Replace with the actual filename of your enrollment dataset
file_path = 'ecd49b12-3084-4521-8f7e-ca8bf72069ba_e47430fe65167fdbd54b769126607714.csv'
df = pd.read_csv(file_path)

print(f"Original Rows: {len(df)}")

# ---------------------------------------------------------
# 2. PRE-PROCESSING
# ---------------------------------------------------------
# A. Convert 'date'
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

# B. Convert 'pincode' to string
df['pincode'] = df['pincode'].astype(str)

# ---------------------------------------------------------
# 3. SOLVING THE FREQUENCY MISMATCH
# ---------------------------------------------------------
# Standardize everything to Monthly sums
df['month_year'] = df['date'].dt.to_period('M')

monthly_df = df.groupby(['month_year', 'state', 'district', 'pincode'])[[ 
    'age_0_5', 'age_5_17', 'age_18_greater' 
]].sum().reset_index()

# Add timestamp for plotting
monthly_df['plot_date'] = monthly_df['month_year'].dt.to_timestamp()
monthly_df['total_enrollments'] = monthly_df['age_0_5'] + monthly_df['age_5_17'] + monthly_df['age_18_greater']

print("\n--- Processed Monthly Enrollment Data ---")
print(monthly_df.head())

# ---------------------------------------------------------
# 4. EXPORT
# ---------------------------------------------------------
monthly_df.to_csv('cleaned_monthly_enrollment_data.csv', index=False)
print("\nSuccess! Saved to 'cleaned_monthly_enrollment_data.csv'")