import pandas as pd

# 1. Load Raw Data
# Replace with your downloaded file name
file_path = '65454dab-1517-40a3-ac1d-47d4dfe6891c_e47430fe65167fdbd54b769126607714.csv' 
df = pd.read_csv(file_path)

print(f"❌ Original Rows: {len(df)}")

# 2. REMOVE DUPLICATES (Critical Step)
df.drop_duplicates(inplace=True)
print(f"✅ Cleaned Rows:  {len(df)}")
print(f"   (Removed {12353 - len(df)} duplicate entries)")

# 3. STANDARDIZE COLUMNS
# Rename 'bio_age_17_' to something readable
df.rename(columns={'bio_age_17_': 'bio_age_above_17'}, inplace=True)

# 4. SAVE CLEAN FILE
output_filename = 'cleaned_monthly_biometric_data.csv'
df.to_csv(output_filename, index=False)
print(f"\n🎉 Success! Saved cleaned data to '{output_filename}'")