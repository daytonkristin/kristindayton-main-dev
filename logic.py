# logic.py - The "Brain" of AV-Sec Architect

def evaluate_risk(device_name, device_type, room_sensitivity):
    """
    Evaluates risk based on Kristin's RMF rules:
    High Sensitivity = Boardrooms, Executive Offices
    Low Sensitivity = Lobby, Hallways
    """
    
    risk_score = "🟢 Low"
    recommendation = "No immediate action required."
    rmf_control = "N/A"

    # Rule 1: Sensitivity Check (Human-in-the-Loop priority)
    if room_sensitivity == "High":
        risk_score = "🔴 High"
        recommendation = "Manual Audit Required: High-sensitivity area."
        rmf_control = "AC-2 (Account Management)"

    # Rule 2: Device-Specific Risk (Default Password check)
    elif "Camera" in device_type:
        risk_score = "🟡 Medium"
        recommendation = "Verify Default Credentials."
        rmf_control = "IA-5 (Authenticator Management)"

    # Rule 3: Legacy Protocol Check
    elif "Old" in device_name:
        risk_score = "🟡 Medium"
        recommendation =
