import streamlit as st
import pandas as pd
import csv, io
from logic import evaluate_risk

# ── Try to import scanner; degrade gracefully if nmap not installed ───────────
try:
    from scanner import scan as _scan
    SCANNER_AVAILABLE = True
except ImportError:
    SCANNER_AVAILABLE = False

st.set_page_config(layout="wide", page_title="AV-Sec Architect")
st.title("🛡️ AV-Sec Architect")
st.caption("NIST RMF Compliance Dashboard for Audiovisual Infrastructure")

# ── Default demo devices ──────────────────────────────────────────────────────
DEMO_DEVICES = [
    {"name": "Boardroom Mic (Sony)",  "ip": "192.168.1.10", "device_type": "Microphone", "room_sensitivity": "High"},
    {"name": "Lobby Camera (Axis)",   "ip": "192.168.1.11", "device_type": "Camera",     "room_sensitivity": "Low"},
    {"name": "Old Display Unit",      "ip": "192.168.1.12", "device_type": "Display",    "room_sensitivity": "Low"},
    {"name": "Office Display",        "ip": "192.168.1.13", "device_type": "Display",    "room_sensitivity": "Low"},
]

if "hosts" not in st.session_state:
    st.session_state.hosts = DEMO_DEVICES.copy()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Add Device")
    with st.form("add_device", clear_on_submit=True):
        name        = st.text_input("Device Name")
        ip          = st.text_input("IP Address")
        device_type = st.selectbox("Type", ["Microphone", "Camera", "Display", "Speaker", "Controller", "Unknown"])
        sensitivity = st.selectbox("Room Sensitivity", ["Low", "High"])
        if st.form_submit_button("Add") and name and ip:
            st.session_state.hosts.append({
                "name": name, "ip": ip,
                "device_type": device_type, "room_sensitivity": sensitivity
            })
            st.success(f"Added {name}")

    st.divider()

    if SCANNER_AVAILABLE:
        st.header("Network Scan")
        target = st.text_input("Target", value="192.168.1.0/24")
        if st.button("Run Scan"):
            with st.spinner("Scanning..."):
                try:
                    found = _scan(target)
                    st.session_state.hosts = found
                    st.success(f"Found {len(found)} devices")
                except Exception as e:
                    st.error(f"Scan failed: {e}")
    else:
        st.info("Network scanner unavailable.\nInstall nmap + python-nmap to enable.")

    if st.button("Reset to Demo Data"):
        st.session_state.hosts = DEMO_DEVICES.copy()

# ── Build risk table ──────────────────────────────────────────────────────────
rows = []
for h in st.session_state.hosts:
    r = evaluate_risk(h["name"], h["device_type"], h["room_sensitivity"])
    rows.append({
        "Severity":    r["risk_score"],
        "Device":      h["name"],
        "IP":          h["ip"],
        "Type":        h["device_type"],
        "Room":        h["room_sensitivity"],
        "Issue":       r["recommendation"],
        "RMF Control": r["rmf_control"],
    })

df = pd.DataFrame(rows)

# ── Summary metrics ───────────────────────────────────────────────────────────
high   = df["Severity"].str.contains("High").sum()
medium = df["Severity"].str.contains("Medium").sum()
low    = df["Severity"].str.contains("Low").sum()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Devices", len(df))
m2.metric("🔴 High",   high)
m3.metric("🟡 Medium", medium)
m4.metric("🟢 Low",    low)

st.divider()

# ── Main layout ───────────────────────────────────────────────────────────────
col1, col2 = st.columns([0.65, 0.35])

with col1:
    st.subheader("Priority Risk List")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Export
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    st.download_button(
        "⬇ Export CSV",
        data=buf.getvalue(),
        file_name="av_sec_report.csv",
        mime="text/csv",
    )

with col2:
    st.subheader("Compliance Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Ask me about any device or risk. Try: 'camera' or 'high risk'"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask about a risk..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        match = df[
            df["Device"].str.contains(prompt, case=False, na=False) |
            df["Issue"].str.contains(prompt, case=False, na=False) |
            df["Severity"].str.contains(prompt, case=False, na=False) |
            df["RMF Control"].str.contains(prompt, case=False, na=False)
        ]

        if not match.empty:
            lines = []
            for _, row in match.iterrows():
                lines.append(f"**{row['Device']}** ({row['IP']}) — {row['Severity']}\n{row['Issue']} · RMF `{row['RMF Control']}`")
            reply = "\n\n".join(lines)
        else:
            reply = "No matching device found. Try a device name, type, or 'high risk'."

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
