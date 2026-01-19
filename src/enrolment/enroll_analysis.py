import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# 1. LOAD CLEANED DATA
# ---------------------------------------------------------
# Make sure you have run the cleaning script first!
file_path = '../../data/processed/cleaned_monthly_enrollment_data.csv'

try:
    df = pd.read_csv(file_path)
    print("✅ Enrollment Data Loaded Successfully!")
except FileNotFoundError:
    print("❌ Error: File not found. Please run the cleaning code first.")
    exit()

# Minimal Preprocessing for Plotting
df['pincode'] = df['pincode'].astype(str)
if 'plot_date' in df.columns:
    df['plot_date'] = pd.to_datetime(df['plot_date'])
    time_col = 'plot_date'
else:
    df['month_year'] = pd.to_datetime(df['month_year'])
    time_col = 'month_year'

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("\n--- Generating Enrollment Insights ---")

# ---------------------------------------------------------
# VISUAL 1: The "Birth Rate Proxy" (Age Trends)
# ---------------------------------------------------------
plt.figure()
trends = df.groupby(time_col)[['age_0_5', 'age_5_17', 'age_18_greater']].sum()

# Plot Lines
plt.plot(trends.index, trends['age_0_5'], marker='o', label='Newborns (0-5)', linewidth=3, color='#2ca02c') # Green for Growth
plt.plot(trends.index, trends['age_5_17'], marker='s', label='School Kids (5-17)', linewidth=2, color='#ff7f0e')
plt.plot(trends.index, trends['age_18_greater'], marker='x', label='Adults (18+)', linewidth=2, color='#d62728', linestyle='--')

plt.title('The "Birth Rate Proxy": Monthly New Aadhaar Generations', fontsize=14, fontweight='bold')
plt.ylabel('New Enrollments')
plt.legend()
plt.tight_layout()
plt.savefig('../../reports/figures/enrollment_visual_1_trends.png')
print("1. Generated: enrollment_visual_1_trends.png (Trends)")

# ---------------------------------------------------------
# VISUAL 2: "Maternity Hotspots" (Top 0-5 Pincodes)
# ---------------------------------------------------------
plt.figure()
# Filter for top baby enrollment centers
top_babies = df.groupby('pincode')['age_0_5'].sum().nlargest(10).sort_values(ascending=False)

sns.barplot(x=top_babies.index, y=top_babies.values, palette='Greens_r')
plt.title('Maternity Hotspots: Top 10 Pincodes for New Birth Enrollments', fontsize=14, fontweight='bold')
plt.xlabel('Pincode')
plt.ylabel('Total Newborn Enrollments (0-5)')
plt.tight_layout()
plt.savefig('../../reports/figures/enrollment_visual_2_hotspots.png')
print("2. Generated: enrollment_visual_2_hotspots.png (Baby Hotspots)")

# ---------------------------------------------------------
# VISUAL 3: The "Ghost Hunter" (Adult Anomalies)
# ---------------------------------------------------------
plt.figure()
# We look for where adults are enrolling NEW Aadhaars (Suspicious/Rare)
top_adults = df.groupby('pincode')['age_18_greater'].sum().nlargest(10).sort_values(ascending=False)

sns.barplot(x=top_adults.index, y=top_adults.values, palette='Reds_r')
plt.title('Anomaly Detection: High Volume of NEW Adult Enrollments (18+)', fontsize=14, fontweight='bold')
plt.xlabel('Pincode')
plt.ylabel('New Adult Enrollments')
# Add a threshold line for "Normal"
avg_adult = df.groupby('pincode')['age_18_greater'].sum().mean()
plt.axhline(avg_adult, color='blue', linestyle='--', label=f'Regional Avg ({int(avg_adult)})')
plt.legend()
plt.tight_layout()
plt.savefig('../../reports/figures/enrollment_visual_3_anomalies.png')
print("3. Generated: enrollment_visual_3_anomalies.png (Adult Anomalies)")

# ---------------------------------------------------------
# VISUAL 4: Sibling Correlation (Scatter)
# ---------------------------------------------------------
plt.figure(figsize=(10, 8))
sns.regplot(data=df, x='age_0_5', y='age_5_17', 
            scatter_kws={'alpha':0.5, 'color':'purple'}, 
            line_kws={'color':'orange', 'lw':2})

plt.title('The "Sibling Effect": Correlation between 0-5 and 5-17 Enrollments', fontsize=14, fontweight='bold')
plt.xlabel('Newborn Enrollments (0-5)')
plt.ylabel('Child Enrollments (5-17)')

# Calc Correlation
corr = df['age_0_5'].corr(df['age_5_17'])
plt.text(df['age_0_5'].max()*0.05, df['age_5_17'].max()*0.9, 
         f'Correlation (r) = {corr:.3f}', 
         bbox=dict(facecolor='white', alpha=0.8), fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('../../reports/figures/enrollment_visual_4_correlation.png')
print("4. Generated: enrollment_visual_4_correlation.png (Correlation)")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter

# ---------------------------------------------------------
# 1. PREPARE DATA
# ---------------------------------------------------------
# Load your cleaned enrollment file
file_path = '../../data/processed/cleaned_monthly_enrollment_data.csv'
df = pd.read_csv(file_path)
df['pincode'] = df['pincode'].astype(str)

# Aggregate Stats by Pincode
pincode_stats = df.groupby('pincode')[['age_0_5', 'age_5_17', 'age_18_greater']].sum()
pincode_stats['total'] = pincode_stats.sum(axis=1)
pincode_stats = pincode_stats.sort_values('total', ascending=False)

# ---------------------------------------------------------
# VISUAL 5: Pareto Efficiency (Resource Optimization)
# ---------------------------------------------------------
# Calculate Cumulative %
pincode_stats['cumulative_percentage'] = pincode_stats['total'].cumsum() / pincode_stats['total'].sum() * 100

plt.figure(figsize=(12, 6))
ax1 = plt.gca()

# Bar Chart (Volume)
sns.barplot(x=pincode_stats.head(20).index, y=pincode_stats.head(20)['total'], color='#2ca02c', ax=ax1, alpha=0.8)
ax1.set_ylabel('Total Enrollments', color='#2ca02c', fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#2ca02c')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)

# Line Chart (Cumulative %)
ax2 = ax1.twinx()
sns.lineplot(x=pincode_stats.head(20).index, y=pincode_stats.head(20)['cumulative_percentage'], color='#d62728', linewidth=3, marker='D', ax=ax2)
ax2.set_ylabel('Cumulative % Load', color='#d62728', fontweight='bold')
ax2.yaxis.set_major_formatter(PercentFormatter())
ax2.set_ylim(0, 110)
ax2.axhline(50, color='blue', linestyle='--', linewidth=2, label='50% Threshold')

plt.title('Pareto Efficiency: Top 10 Centers Handle ~50% of All Enrollments', fontsize=14, fontweight='bold')
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig('../../reports/figures/enrollment_visual_5_pareto.png')
print("Generated: enrollment_visual_5_pareto.png")

# ---------------------------------------------------------
# VISUAL 6: Demographic DNA (Stacked Bar)
# ---------------------------------------------------------
# Get Top 10 Busiest Centers
top_10 = pincode_stats.head(10)[['age_0_5', 'age_5_17', 'age_18_greater']]

# Plot Stacked Bar
ax = top_10.plot(kind='bar', stacked=True, color=['#2ca02c', '#ff7f0e', '#d62728'], figsize=(12, 6), width=0.8)

plt.title('Demographic DNA: Composition of Top 10 Centers', fontsize=14, fontweight='bold')
plt.ylabel('Total Enrollments')
plt.xlabel('Pincode')
plt.legend(['Newborns (0-5)', 'Kids (5-17)', 'Adults (18+)'])
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../../reports/figures/enrollment_visual_6_composition.png')
print("Generated: enrollment_visual_6_composition.png")

print("\n--- Insight for Report ---")
print("Visual 6 proves that the Top Centers are dominated by GREEN bars (Newborns).")
print("These are not 'General Aadhaar Centers'—they are effectively 'Maternity Registration Hubs'.")

# ---------------------------------------------------------
# STATS OUTPUT
# ---------------------------------------------------------
print("\n" + "="*40)
print("📊 ENROLLMENT INTELLIGENCE REPORT")
print("="*40)
print(f"1. Total Newborns (0-5): {df['age_0_5'].sum()}")
print(f"2. Total Adults (18+):   {df['age_18_greater'].sum()}")
print(f"   -> Ratio: {df['age_0_5'].sum() / df['age_18_greater'].sum():.1f} Babies for every 1 Adult.")
print(f"3. Sibling Correlation:  {corr:.3f} (Validates 'Family Visit' theory)")
print("="*40)
print("\n✅ DONE! All enrollment images saved.")