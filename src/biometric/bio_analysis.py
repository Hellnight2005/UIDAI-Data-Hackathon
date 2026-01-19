import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter

# ==========================================
# 1. LOAD CLEANED DATA
# ==========================================
# Ensure you run 'clean_biometrics.py' first!
file_path = '../../data/processed/cleaned_monthly_biometric_data.csv'

try:
    df = pd.read_csv(file_path)
    print("✅ Loaded Cleaned Biometric Data.")
except FileNotFoundError:
    print("❌ Error: 'cleaned_monthly_biometric_data.csv' not found.")
    print("   Run the preprocessing script first!")
    exit()

# ---------------------------------------------------------
# 🚨 THE FIX IS HERE: Add dayfirst=True
# ---------------------------------------------------------
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

# Continue Preprocessing
df['pincode'] = df['pincode'].astype(str)
df['month_year'] = df['date'].dt.to_period('M')

# Aggregate to Monthly Level
monthly_df = df.groupby(['month_year', 'pincode'])[[
    'bio_age_5_17', 'bio_age_above_17'
]].sum().reset_index()

monthly_df['plot_date'] = monthly_df['month_year'].dt.to_timestamp()
monthly_df['total'] = monthly_df['bio_age_5_17'] + monthly_df['bio_age_above_17']

# ==========================================
# 2. GENERATE VISUALIZATIONS
# ==========================================
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("\n--- Generating Visuals ---")

# --- VISUAL 1: The "Mandatory" Surge (Trends) ---
plt.figure()
trends = monthly_df.groupby('plot_date')[['bio_age_5_17', 'bio_age_above_17']].sum()
plt.plot(trends.index, trends['bio_age_5_17'], marker='s', label='Mandatory (Kids 5-17)', color='#ff7f0e', linewidth=3)
plt.plot(trends.index, trends['bio_age_above_17'], marker='o', label='Voluntary (Adults 17+)', color='#1f77b4', linewidth=2, linestyle='--')
plt.title('Biometric Update Trends: The "Mandatory" Load (Kids) vs. Adults', fontsize=14, fontweight='bold')
plt.ylabel('Transactions')
plt.legend()
plt.tight_layout()
plt.savefig('../../reports/figures/biometric_visual_1_trends.png')
print("1. Generated: biometric_visual_1_trends.png")

# --- VISUAL 2: The "Triple-Threat" Check (Bottlenecks) ---
plt.figure()
top_centers = monthly_df.groupby('pincode')['total'].sum().nlargest(10).sort_values(ascending=False)
sns.barplot(x=top_centers.index, y=top_centers.values, palette='magma')
plt.title('Biometric Bottlenecks: Top 10 High-Volume Centers', fontsize=14, fontweight='bold')
plt.xlabel('Pincode')
plt.ylabel('Total Volume')
plt.tight_layout()
plt.savefig('../../reports/figures/biometric_visual_2_bottlenecks.png')
print("2. Generated: biometric_visual_2_bottlenecks.png")

# --- VISUAL 3: Correlation (The School Run) ---
plt.figure(figsize=(8, 8))
sns.regplot(data=monthly_df, x='bio_age_above_17', y='bio_age_5_17', 
            scatter_kws={'alpha':0.5, 'color':'purple'}, line_kws={'color':'orange'})
plt.title('Correlation: Adult vs Child Updates', fontsize=14, fontweight='bold')
plt.xlabel('Adult Updates')
plt.ylabel('Child Updates (Mandatory)')
# Add Score
corr = monthly_df['bio_age_above_17'].corr(monthly_df['bio_age_5_17'])
plt.text(monthly_df['bio_age_above_17'].max()*0.05, monthly_df['bio_age_5_17'].max()*0.9, 
         f'Correlation (r) = {corr:.3f}', bbox=dict(facecolor='white', alpha=0.8), fontsize=12)
plt.tight_layout()
plt.savefig('../../reports/figures/biometric_visual_3_correlation.png')
print("3. Generated: biometric_visual_3_correlation.png")

# --- VISUAL 4: Pareto Efficiency (Concentration) ---
# Prepare Data
pincode_stats = monthly_df.groupby('pincode')['total'].sum().sort_values(ascending=False).reset_index()
pincode_stats['cumulative_percentage'] = pincode_stats['total'].cumsum() / pincode_stats['total'].sum() * 100

plt.figure()
ax1 = plt.gca()
sns.barplot(x=pincode_stats.head(20)['pincode'], y=pincode_stats.head(20)['total'], color='#663399', ax=ax1, alpha=0.8)
ax1.set_ylabel('Total Updates', color='#663399', fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#663399')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)

ax2 = ax1.twinx()
sns.lineplot(x=pincode_stats.head(20)['pincode'], y=pincode_stats.head(20)['cumulative_percentage'], color='#ff7f0e', linewidth=3, marker='D', ax=ax2)
ax2.set_ylabel('Cumulative % Load', color='#ff7f0e', fontweight='bold')
ax2.yaxis.set_major_formatter(PercentFormatter())
ax2.set_ylim(0, 110)
ax2.axhline(50, color='green', linestyle='--', linewidth=2, label='50% Threshold')

plt.title('Pareto Analysis: Top Centers Handle Half the Load', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('../../reports/figures/biometric_visual_4_pareto.png')
print("4. Generated: biometric_visual_4_pareto.png")

# --- VISUAL 5: Demographic Split (Stacked Bar) ---
plt.figure()
top_10_codes = pincode_stats.head(10)['pincode']
subset = monthly_df[monthly_df['pincode'].isin(top_10_codes)].groupby('pincode')[['bio_age_5_17', 'bio_age_above_17']].sum()
subset = subset.loc[top_10_codes] # Sort by total volume

subset.plot(kind='bar', stacked=True, color=['#ff7f0e', '#1f77b4'], figsize=(12, 6))
plt.title('Demographic Split: Mandatory (Orange) vs Voluntary (Blue)', fontsize=14, fontweight='bold')
plt.xlabel('Pincode')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../../reports/figures/biometric_visual_5_split.png')
print("5. Generated: biometric_visual_5_split.png")

# ==========================================
# 3. STATISTICAL REPORT
# ==========================================
print("\n" + "="*40)
print("📊 BIOMETRIC INTELLIGENCE REPORT")
print("="*40)
print(f"1. Total Mandatory Updates (Kids): {monthly_df['bio_age_5_17'].sum()}")
print(f"2. Total Voluntary Updates (Adults): {monthly_df['bio_age_above_17'].sum()}")
ratio = monthly_df['bio_age_5_17'].sum() / monthly_df['bio_age_above_17'].sum()
print(f"   -> Ratio: {ratio:.2f} Kids for every 1 Adult.")
print(f"3. Correlation Score: {corr:.3f}")
print(f"4. Busiest Center: {pincode_stats.iloc[0]['pincode']} ({pincode_stats.iloc[0]['total']} updates)")
print("="*40)
print("\n✅ DONE! All 5 biometric visuals saved.")