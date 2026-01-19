incode-wise Demographic Analysis (Children & Adults)
📌 Project Overview

This project performs exploratory data analysis (EDA) and time-based population insights using survey data collected across different pincodes.
The analysis focuses on:

Children population (Age 5–17)

Adult population (Age 18+)

Survey frequency per pincode

Trends over time

The objective is to identify reliable pincodes, clean noisy data, detect anomalies, and generate meaningful insights for decision-making.



🛠 Tools & Libraries Used

Python

Pandas – Data cleaning, transformation, aggregation

NumPy – Numerical operations

Matplotlib – Visualization

Seaborn – Statistical plots



📂 Dataset Loading
df = pd.read_csv("newfileanal.csv")


Imported the dataset from a CSV file.

Used df.head() to verify structure and columns.

🔍 Missing Value Analysis
df.isna().sum()


Checked missing values column-wise.

Ensured data quality before analysis.

📦 Outlier Detection (Children 5–17)
sns.boxplot(df['bio_age_5_17'])

Why?

To detect extreme or unrealistic values.

Boxplots visually identify outliers affecting statistical accuracy.

📊 Value Distribution Check
for i in df.columns:
    print(df[i].value_counts())

Purpose:

Understand frequency distribution.

Identify categorical dominance or data imbalance.

🧹 Data Cleaning
Removed irrelevant columns:
df.drop(columns=['state', 'district'], inplace=True)

Converted date column:
df['date'] = pd.to_datetime(df['date'], format="%d-%m-%Y")

Extracted time features:
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

📦 Adult Population Outlier Handling
sns.boxplot(df['bio_age_17_'])

Removed unrealistic values:
df = df[df['bio_age_17_'] <= 400]
df = df[df['bio_age_5_17'] <= 240]

Why?

Prevent human-entry errors from distorting analysis.

Improves reliability of aggregated results.

🔢 Year Encoding
df = pd.get_dummies(df, columns=['year'], dtype='uint8')

Purpose:

Make data machine-learning ready

Preserve time-related patterns

📍 Pincode Reliability Filtering
df = df[df['pincode'].isin(df['pincode'].value_counts()[lambda x: x > 25].index)]

Why?

Ensures only frequently surveyed pincodes are used.

Avoids insights from insufficient data.

📊 Aggregated Insights by Pincode
insight_df = df.groupby('pincode').agg(
    pinocde_count=('pincode', 'count'),
    all_children_count=('bio_age_5_17', 'sum'),
    all_adult_count=('bio_age_17_', 'sum')
).reset_index()

Generated:

Total children population

Total adult population

Survey frequency per pincode

⚠️ Anomaly Detection
insight_df = insight_df[insight_df['pincode'] != 400096]

Reason:

Pincode 400096 had unrealistically low population.

Likely human data entry error.

🏆 Key Findings
Most populated:
most_children_pincode = insight_df['all_children_count'].idxmax()
most_adult_pincode = insight_df['all_adult_count'].idxmax()

Least populated:
low_adult_pincode = insight_df['all_adult_count'].idxmin()

📈 Time-Series Trend Analysis
plt.plot(temp['date'], temp['bio_age_5_17'])
plt.plot(temp['date'], temp['bio_age_17_'])

Purpose:

Track population changes over time per pincode.

Identify growth, decline, or stability patterns.

📊 Visual Comparisons
Children vs Adults:
plt.bar(x, insight_df["all_children_count"])
plt.bar(x + width, insight_df["all_adult_count"])

Survey Coverage:
plt.bar(x, insight_df["pinocde_count"])

💡 Value of This Analysis

✔ Identifies reliable pincodes
✔ Detects data quality issues
✔ Helps in policy planning & resource allocation
✔ Useful for NGOs, healthcare planning, education planning
✔ Ready foundation for predictive modeling

🚀 Future Enhancements

Add population growth forecasting

Integrate geographic mapping

Apply clustering for pincode segmentation

Build dashboards using Power BI / Tableau