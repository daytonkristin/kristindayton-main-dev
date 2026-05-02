import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from logic import evaluate_risk

def test_high_sensitivity_always_high():
    r = evaluate_risk("Any Device", "Microphone", "High")
    assert r["risk_score"] == "🔴 High"
    assert r["rmf_control"] == "AC-2"

def test_camera_medium_risk():
    r = evaluate_risk("Lobby Cam", "Camera", "Low")
    assert r["risk_score"] == "🟡 Medium"
    assert r["rmf_control"] == "IA-5"

def test_legacy_device_medium_risk():
    r = evaluate_risk("Old Projector", "Display", "Low")
    assert r["risk_score"] == "🟡 Medium"
    assert r["rmf_control"] == "SI-2"

def test_default_low_risk():
    r = evaluate_risk("Office Display", "Display", "Low")
    assert r["risk_score"] == "🟢 Low"
    assert r["rmf_control"] == "N/A"

def test_high_sensitivity_overrides_camera():
    # High sensitivity room beats camera rule
    r = evaluate_risk("Exec Camera", "Camera", "High")
    assert r["risk_score"] == "🔴 High"
