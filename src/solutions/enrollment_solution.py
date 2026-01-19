def assign_queue_priority(user_type, group_size, location):
    """
    Determines the queue assignment based on demographics and location risk.
    """
    
    # 1. PRIORITY: Infants get the fastest lane (prevents crying/delay)
    if user_type == "New Enrollment (0-5)":
        return "🟢 Priority Lane – Infants"
    
    # 2. EFFICIENCY: Families go to a counter that can handle groups
    elif user_type == "Family" and group_size > 1:
        return "🔵 Family Counter"
    
    # 3. SECURITY: High-risk anomaly detection (based on your chart data for 400072)
    elif user_type == "New Adult (18+)" and location == "400072":
        return "🔴 Manual Verification Required"
    
    # 4. STANDARD: Everyone else goes to the general queue
    else:
        return "⚪ Standard Queue"

# --- Testing the Logic (Examples) ---
print(assign_queue_priority("New Enrollment (0-5)", 1, "400050")) 
# Output: 🟢 Priority Lane – Infants

print(assign_queue_priority("Family", 3, "400050"))
# Output: 🔵 Family Counter

print(assign_queue_priority("New Adult (18+)", 1, "400072"))
# Output: 🔴 Manual Verification Required

print(assign_queue_priority("Update", 1, "400099"))
# Output: ⚪ Standard Queue