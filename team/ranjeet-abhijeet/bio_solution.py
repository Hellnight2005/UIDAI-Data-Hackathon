import pandas as pd
import math

# ==========================================
# ⚙️ SYSTEM INITIALIZATION
# ==========================================
FILE_PATH = 'cleaned_monthly_biometric_data.csv'

print("🔄 Initializing 'School Camp Scheduler' Protocol...")

try:
    # 1. Load the Knowledge Base
    df = pd.read_csv(FILE_PATH)
    df['pincode'] = df['pincode'].astype(str)
    
    # 2. Compute "School Cluster" Intelligence
    # We identify areas where Child Updates (Mandatory) are the dominant strain
    pincode_stats = df.groupby('pincode')[['bio_age_5_17', 'bio_age_above_17']].sum()
    
    # Threshold: A "School Cluster" is any area with > 2,000 child updates annually
    # (Justification: 2000 kids = ~10 schools. Worth sending a van.)
    SCHOOL_CLUSTER_THRESHOLD = 2000 
    
    # Capacity of one Mobile Biometric Kit (Students processed per day)
    KIT_CAPACITY_DAILY = 60 
    
    print(f"✅ System Online!")
    print(f"📊 Threshold for Camp Deployment: > {SCHOOL_CLUSTER_THRESHOLD} students/year")
    print("---------------------------------------------------\n")

except FileNotFoundError:
    print(f"❌ ERROR: Could not find '{FILE_PATH}'. Run the biometric analysis first.")
    exit()

# ==========================================
# 🧠 LOGIC ENGINE: THE CAMP SCHEDULER
# ==========================================
def deploy_unit(pincode):
    pincode = str(pincode).strip()
    
    if pincode not in pincode_stats.index:
        return {
            "status": "UNKNOWN",
            "message": "Pincode not found in database.",
            "color": "gray"
        }
        
    stats = pincode_stats.loc[pincode]
    child_vol = int(stats['bio_age_5_17'])
    adult_vol = int(stats['bio_age_above_17'])
    
    # LOGIC: Do we send a van?
    if child_vol > SCHOOL_CLUSTER_THRESHOLD:
        # Calculate Logistics
        total_days_needed = math.ceil(child_vol / KIT_CAPACITY_DAILY)
        kits_recommended = math.ceil(total_days_needed / 5) # Assume a 5-day "Camp Week"
        
        return {
            "status": "🚨 DEPLOY MOBILE UNIT",
            "message": f"High Concentration of Students detected ({child_vol} mandatory updates).",
            "action": f"LOGISTICS: Deploy {kits_recommended} Mobile Kits for 1 Week.",
            "impact": f"📉 Center Relief: Will reduce footfall at center by {child_vol} visits.",
            "color": "red"
        }
    
    else:
        return {
            "status": "✅ STANDARD OPERATION",
            "message": f"Student volume is manageable ({child_vol} updates).",
            "action": "ACTION: Redirect students to nearest Permanent Center.",
            "impact": "No mobile intervention required.",
            "color": "green"
        }

# ==========================================
# 🚀 INTERACTIVE DEMO LOOP
# ==========================================
if __name__ == "__main__":
    print("DEMO MODE: School Cluster Identification System\n")
    
    while True:
        print("\n" + "-"*30)
        pincode_in = input("Enter Area Pincode (e.g., 400043, 400050): ")
        if pincode_in.lower() == 'q': break
        
        # Run Logic
        result = deploy_unit(pincode_in)
        
        # Display Result
        print("\n" + "="*40)
        print(f"DECISION: {result['status']}")
        print("="*40)
        print(result['message'])
        print(result['action'])
        if 'impact' in result:
            print(f"BENEFIT: {result['impact']}")