import pandas as pd
import numpy as np

# ==========================================
# ⚙️ SYSTEM INITIALIZATION
# ==========================================
FILE_PATH = 'cleaned_monthly_enrollment_data.csv'

print("🔄 Initializing 'Family-First' Smart Queue System...")

try:
    # 1. Load the Knowledge Base
    df = pd.read_csv(FILE_PATH)
    df['pincode'] = df['pincode'].astype(str)
    
    # 2. Compute Risk & Priority Profiles
    # Identify "Maternity Hubs" (Top 20% by Newborn Volume)
    newborn_stats = df.groupby('pincode')['age_0_5'].sum()
    maternity_threshold = newborn_stats.quantile(0.80)
    maternity_hubs = newborn_stats[newborn_stats > maternity_threshold].index.tolist()
    
    # Identify "Fraud Risk Zones" (Top 5% by Adult Volume)
    # High adult enrollment is rare/suspicious in Mumbai
    adult_stats = df.groupby('pincode')['age_18_greater'].sum()
    fraud_threshold = adult_stats.quantile(0.95)
    fraud_zones = adult_stats[adult_stats > fraud_threshold].index.tolist()
    
    print(f"✅ System Online!")
    print(f"👶 Maternity Hubs Identified: {len(maternity_hubs)} centers")
    print(f"🚩 Fraud Risk Zones Identified: {len(fraud_zones)} centers")
    print("---------------------------------------------------\n")

except FileNotFoundError:
    print(f"❌ ERROR: Could not find '{FILE_PATH}'. Run the analysis first.")
    exit()

# ==========================================
# 🧠 SMART QUEUE LOGIC ENGINE
# ==========================================
def assign_queue(pincode, age_group, family_size):
    pincode = str(pincode).strip()
    
    # Context Check
    is_maternity_hub = pincode in maternity_hubs
    is_risk_zone = pincode in fraud_zones
    
    print(f"\n--- Processing User at Center {pincode} ---")
    
    # LOGIC 1: THE "GHOST HUNTER" (Fraud Prevention)
    # If an Adult is enrolling in a High-Risk Zone, trigger security check.
    if age_group == "Adult (18+)" and is_risk_zone:
        return {
            "queue": "🛑 SECURITY CHECK",
            "message": f"ALERT: High volume of adult enrollments detected in {pincode}.",
            "action": "ACTION: Require 2-Level Document Verification (Supervisor Approval).",
            "color": "red"
        }
    
    # LOGIC 2: THE "MATERNITY EXPRESS" (Infant Priority)
    # If it's a baby, give them the Tablet Station (Fast Track).
    if age_group == "Newborn (0-5)":
        return {
            "queue": "👶 PRIORITY LANE A",
            "message": "Detected Infant Enrollment.",
            "action": "ASSIGNMENT: Direct to Tablet Station #1 (Child-Friendly).",
            "color": "green"
        }
        
    # LOGIC 3: THE "FAMILY BUNDLE" (Sibling Effect)
    # If family size > 1, put them in a Double Booth so they don't block the line twice.
    if family_size > 1:
        return {
            "queue": "👨‍👩‍👧 FAMILY BOOTH",
            "message": f"Family Group of {family_size} detected.",
            "action": "ASSIGNMENT: Open Double-Seater Booth. Process all IDs in one session.",
            "color": "blue"
        }
        
    # LOGIC 4: STANDARD
    return {
        "queue": "Standard Queue",
        "message": "Routine Enrollment.",
        "action": "Please wait for your token number.",
        "color": "white"
    }

# ==========================================
# 🚀 INTERACTIVE DEMO LOOP
# ==========================================
if __name__ == "__main__":
    print("DEMO MODE: Simulation of Kiosk Logic\n")
    
    while True:
        print("\n" + "-"*30)
        pincode_in = input("1. Enter Center Pincode (e.g., 400043, 400072): ")
        if pincode_in.lower() == 'q': break
        
        print("2. Select Applicant Type:")
        print("   [A] Newborn (0-5)")
        print("   [B] Child (5-17)")
        print("   [C] Adult (18+)")
        type_in = input("   Selection: ").upper()
        
        mapper = {'A': 'Newborn (0-5)', 'B': 'Child (5-17)', 'C': 'Adult (18+)'}
        if type_in not in mapper: continue
        age_cat = mapper[type_in]
        
        size_in = int(input("3. Total Family Members present: "))
        
        # Run Logic
        result = assign_queue(pincode_in, age_cat, size_in)
        
        # Display Result
        print("\n" + "="*40)
        print(f"🎫 TICKET: {result['queue']}")
        print("="*40)
        print(result['message'])
        print(result['action'])