import pandas as pd
import numpy as np

# ==========================================
# ⚙️ CONFIGURATION & DATA LOADING
# ==========================================
FILE_PATH = 'cleaned_monthly_uidai_data.csv'

print("🔄 Initializing Aadhaar Smart-Flow System...")

try:
    # Load the historical data
    df = pd.read_csv(FILE_PATH)
    
    # Preprocessing: Ensure Pincode is treated as a string (ID), not a number
    df['pincode'] = df['pincode'].astype(str)
    
    # Calculate the "Load Score" for each center
    # We use the AVERAGE monthly volume to determine typical stress levels
    if 'total_updates' not in df.columns:
        df['total_updates'] = df['demo_age_5_17'] + df['demo_age_above_17']
        
    center_stats = df.groupby('pincode')['total_updates'].mean().sort_values(ascending=False)
    
    # Define the "High Stress" Threshold (Top 20% of centers)
    # Any center with traffic higher than this number is a "RED ZONE"
    stress_threshold = center_stats.quantile(0.80)
    
    print(f"✅ System Ready! Database contains {len(center_stats)} centers.")
    print(f"📊 High-Traffic Threshold: > {stress_threshold:.0f} users/month")
    print("---------------------------------------------------\n")

except FileNotFoundError:
    print(f"❌ ERROR: Could not find '{FILE_PATH}'.")
    print("Please make sure the cleaned CSV file is in the same folder.")
    exit()

# ==========================================
# 🧠 THE SMART LOGIC ENGINE
# ==========================================
def find_slot(user_pincode):
    user_pincode = str(user_pincode).strip()
    
    # 1. VALIDATION: Does the center exist?
    if user_pincode not in center_stats.index:
        return {
            "status": "ERROR",
            "message": "Pincode not found in Mumbai Suburban database.",
            "color": "gray"
        }
    
    current_load = center_stats[user_pincode]
    
    # 2. DECISION: Is it a "Red Zone"?
    if current_load > stress_threshold:
        # LOGIC: Find the best alternative
        # In a real app, this would use GPS coordinates to find the *nearest* one.
        # For this Hackathon demo, we find the *lowest traffic* center in the list.
        recommendation = center_stats.idxmin() # Finds the center with lowest load
        rec_load = center_stats.min()
        
        time_saved = (current_load - rec_load) / 10 # Rough estimate: 10 users = 1 min wait
        
        return {
            "status": "HIGH CONGESTION",
            "message": f"⚠️ Pincode {user_pincode} is Overloaded ({int(current_load)} users/mo).",
            "action": f"💡 ROUTING: Go to Center {recommendation} instead.",
            "benefit": f"📉 Traffic there: {int(rec_load)} users (Empty). Est. Time Saved: {int(time_saved)} mins.",
            "color": "red"
        }
    
    else:
        return {
            "status": "GREEN ZONE",
            "message": f"✅ Pincode {user_pincode} has normal traffic ({int(current_load)} users/mo).",
            "action": "You can proceed to this center.",
            "benefit": "Expected Wait Time: < 15 mins",
            "color": "green"
        }

# ==========================================
# 🚀 INTERACTIVE DEMO LOOP
# ==========================================
if __name__ == "__main__":
    while True:
        user_input = input("Enter your Pincode (or 'q' to quit): ")
        if user_input.lower() == 'q':
            print("Exiting System.")
            break
            
        result = find_slot(user_input)
        
        # Pretty Print the Output
        print("\n" + "="*40)
        print(f"STATUS: {result['status']}")
        print("-" * 40)
        print(result['message'])
        if 'action' in result:
            print(result['action'])
        if 'benefit' in result:
            print(result['benefit'])
        print("="*40 + "\n")