import pandas as pd
import numpy as np

# ==========================================
# 1. SETUP & MOCK DATA (Simulating your CSV)
# ==========================================
# In your real code, you will use: df = pd.read_csv('cleaned_monthly_uidai_data.csv')
print("🔄 Initializing Combined Smart-System...")

# Creating fake data to demonstrate the logic works
data = {
    'pincode': ['400050', '400072', '400099', '400001'],
    'total_updates': [120, 5000, 300, 80] # 400072 is very high traffic
}
df = pd.DataFrame(data)
center_stats = df.set_index('pincode')['total_updates']
stress_threshold = 2000  # Arbitrary threshold for this demo

# ==========================================
# 2. STAGE 1: LOAD BALANCING (The Routing Logic)
# ==========================================
def check_center_load(pincode):
    pincode = str(pincode).strip()
    
    if pincode not in center_stats.index:
        return "UNKNOWN"
        
    load = center_stats[pincode]
    
    if load > stress_threshold:
        # Recommendation Logic
        best_center = center_stats.idxmin()
        return {
            "status": "OVERLOADED",
            "msg": f"⚠️ High Traffic ({load} users). Go to {best_center} instead!",
            "allow_entry": False # Suggest they leave, but we can override
        }
    else:
        return {
            "status": "NORMAL",
            "msg": "✅ Traffic is Normal. Proceeding to Queue...",
            "allow_entry": True
        }

# ==========================================
# 3. STAGE 2: PRIORITY QUEUE (The Lane Logic)
# ==========================================
def assign_queue_priority(user_type, group_size, location):
    # Infant Priority
    if user_type == "New Enrollment (0-5)":
        return "🟢 Priority Lane – Infants"
    
    # Family Efficiency
    elif user_type == "Family" and group_size > 1:
        return "🔵 Family Counter"
    
    # Security Anomaly Check (The 400072 Logic)
    elif user_type == "New Adult (18+)" and location == "400072":
        return "🔴 Manual Verification Required"
    
    # Standard
    else:
        return "⚪ Standard Queue"

# ==========================================
# 4. MASTER EXECUTION LOOP
# ==========================================
def run_kiosk_demo():
    print("\n--- WELCOME TO AADHAAR SMART KIOSK ---")
    
    # Step 1: Check Location
    loc = input("Enter current Pincode: ")
    load_status = check_center_load(loc)
    
    if load_status == "UNKNOWN":
        print("❌ Center not found.")
        return

    print(f"\n[SYSTEM]: {load_status['msg']}")
    
    # If overloaded, ask user if they still want to stay
    if load_status['status'] == "OVERLOADED":
        choice = input("Stay here anyway? (y/n): ")
        if choice.lower() != 'y':
            print("Redirecting you to new center... Goodbye!")
            return

    # Step 2: If they stay, assign Queue
    print("\n--- ENTER DEMOGRAPHICS ---")
    u_type = input("Type (New Enrollment (0-5), Family, New Adult (18+), Update): ")
    g_size = int(input("Group Size (1-10): "))
    
    token = assign_queue_priority(u_type, g_size, loc)
    
    print("\n" + "="*30)
    print(f"🎫 YOUR TOKEN: {token}")
    print("="*30)

# Run the demo
if __name__ == "__main__":
    run_kiosk_demo()