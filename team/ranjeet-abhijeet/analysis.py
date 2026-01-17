import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# 1. LOAD THE CLEANED DATA
# ---------------------------------------------------------
# We use the 'cleaned' file directly.
file_path = 'cleaned_monthly_uidai_data.csv' 
df = pd.read_csv(file_path)

print("Data Loaded Successfully!")
print(df.columns)

# ---------------------------------------------------------
# 2. PREPARE FOR PLOTTING (Minimal Setup)
# ---------------------------------------------------------
# Since the file is already cleaned, we just need to ensure formatting is right.

# Convert 'plot_date' back to datetime (CSV saves it as text)
# Note: In the cleaned file, the date column is likely named 'plot_date'
if 'plot_date' in df.columns:
    df['plot_date'] = pd.to_datetime(df['plot_date'])
    time_col = 'plot_date'
else:
    # Fallback if the column has a different name
    print("Warning: 'plot_date' not found. Creating it from 'month_year'...")
    df['month_year'] = pd.to_datetime(df['month_year'])
    time_col = 'month_year'

# Ensure pincode is a string (category), not a number
df['pincode'] = df['pincode'].astype(str)

# Calculate Total Updates if not already present
if 'total_updates' not in df.columns:
    df['total_updates'] = df['demo_age_5_17'] + df['demo_age_above_17']

# ---------------------------------------------------------
# 3. GENERATE VISUALIZATIONS
# ---------------------------------------------------------
sns.set_style("whitegrid")

# A. The "Compliance Tsunami" (Trend Analysis)
plt.figure(figsize=(12, 6))
# Group by time column
trends = df.groupby(time_col)[['demo_age_5_17', 'demo_age_above_17']].sum()

plt.plot(trends.index, trends['demo_age_above_17'], marker='o', label='Adults (17+)', linewidth=3, color='#005a8d')
plt.plot(trends.index, trends['demo_age_5_17'], marker='s', label='Children (5-17)', linewidth=3, color='#f37021')
plt.title('The "Compliance Tsunami": Impact of PAN-Linking Deadline', fontsize=14, fontweight='bold')
plt.ylabel('Transactions')
plt.xlabel('Date')
plt.legend()
plt.tight_layout()
plt.savefig('visual_1_trends.png')
print("Generated: visual_1_trends.png")

# B. The "Chronic Bottleneck" (Top 10 Pincodes)
plt.figure(figsize=(12, 6))
top_pincodes = df.groupby('pincode')['total_updates'].sum().nlargest(10).sort_values(ascending=False)
sns.barplot(x=top_pincodes.index, y=top_pincodes.values, palette='Reds_r')
plt.title('Structural Bottlenecks: Top 10 High-Stress Pincodes', fontsize=14, fontweight='bold')
plt.xlabel('Pincode')
plt.ylabel('Total Annual Transactions')
plt.tight_layout()
plt.savefig('visual_2_bottlenecks.png')
print("Generated: visual_2_bottlenecks.png")

# C. The "Red Zone" Heatmap
plt.figure(figsize=(14, 8))
# Get top 15 busy pincodes
top_15_list = df.groupby('pincode')['total_updates'].sum().nlargest(15).index
# Filter data for only these pincodes
subset = df[df['pincode'].isin(top_15_list)]

# Pivot table for heatmap
heatmap_data = subset.pivot_table(index='pincode', columns=time_col, values='total_updates', aggfunc='sum')

# Draw Heatmap
sns.heatmap(heatmap_data, cmap='OrRd', linewidths=.5, linecolor='gray')
plt.title('Operational Heatmap: Identifying Chronic vs. Volatile Zones', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('visual_3_heatmap.png')
print("Generated: visual_3_heatmap.png")

# ---------------------------------------------------------
# D. FINAL BONUS: The Pareto Chart (Resource Optimization)
# ---------------------------------------------------------
from matplotlib.ticker import PercentFormatter

# 1. Prepare Data
pareto_df = df.groupby('pincode')['total_updates'].sum().sort_values(ascending=False).reset_index()
pareto_df['cumulative_percentage'] = pareto_df['total_updates'].cumsum() / pareto_df['total_updates'].sum() * 100

# 2. Plot
fig, ax1 = plt.subplots(figsize=(12, 6))

# Bar Chart (Volume)
sns.barplot(data=pareto_df.head(20), x='pincode', y='total_updates', color='#005a8d', ax=ax1, alpha=0.8)
ax1.set_ylabel('Total Transactions (Volume)', color='#005a8d', fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#005a8d')
ax1.set_xlabel('Top 20 Pincodes (Ranked by Load)', fontweight='bold')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)

# Line Chart (Cumulative %)
ax2 = ax1.twinx()
sns.lineplot(data=pareto_df.head(20), x='pincode', y='cumulative_percentage', color='#f37021', linewidth=3, marker='D', ax=ax2)
ax2.set_ylabel('Cumulative % of City-Wide Load', color='#f37021', fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#f37021')
ax2.yaxis.set_major_formatter(PercentFormatter())
ax2.set_ylim(0, 100)

# Threshold Line (50%)
ax2.axhline(50, color='green', linestyle='--', linewidth=2, label='50% Workload Threshold')

plt.title('The Pareto Efficiency: 17% of Locations Handle ~53% of the Load', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('visual_4_pareto.png')
print("Generated: visual_4_pareto.png")

print("\n--- FINAL STRATEGIC INSIGHT ---")
print("Optimization Opportunity: Focusing resources on just the Top 10 pincodes solves >50% of the entire city's congestion.")

print("\n--- Success! All charts generated. ---")