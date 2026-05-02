# logic.py - Risk evaluation engine for AV-Sec Architect

def evaluate_risk(device_name: str, device_type: str, room_sensitivity: str) -> dict:
    """
    Evaluates risk based on NIST RMF rules.
    Returns: {risk_score, recommendation, rmf_control}
    """
    # Rule 1: High-sensitivity room → always High
    if room_sensitivity == "High":
        return {
            "risk_score": "🔴 High",
            "recommendation": "Manual Audit Required: High-sensitivity area.",
            "rmf_control": "AC-2",
        }

    # Rule 2: Camera with likely default credentials
    if "Camera" in device_type:
        return {
            "risk_score": "🟡 Medium",
            "recommendation": "Verify and rotate default credentials.",
            "rmf_control": "IA-5",
        }

    # Rule 3: Legacy device (flagged by name)
    if "Old" in device_name or "Legacy" in device_name:
        return {
            "risk_score": "🟡 Medium",
            "recommendation": "Review legacy protocol usage; plan upgrade.",
            "rmf_control": "SI-2",
        }

    # Default: Low risk
    return {
        "risk_score": "🟢 Low",
        "recommendation": "No immediate action required.",
        "rmf_control": "N/A",
    }
