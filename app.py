import streamlit as st
import pandas as pd
from logic import evaluate_risk
from scanner import scan

st.set_page_config(layout="wide", page_title="AV-Sec Architect")
st.title("🛡️ AV-Sec Architect: Compliance Dashboard")

# ── Sidebar: scan controls ────────────────────────────────────────────────────
with st.sidebar:
    st.header("Scanner")
    target = st.text_input("Target", value="127.0.0.1")
    if st.button("Run Scan"):
        st.session_state.hosts = scan(target)

# Seed with example data if no scan has run yet
if "hosts" not in st.session_state:
    st.session_state.hosts = [
        {"name": "Boardroom Mic (Sony)",  "ip": "192.168.1.10", "status": "up", "device_type": "Microphone", "room_sensitivity": "High"},
        {"name": "Lobby Camera (Axis)",   "ip": "192.168.1.11", "status": "up", "device_type": "Camera",     "room_sensitivity": "Low"},
        {"name": "Old Display Unit",      "ip": "192.168.1.12", "status": "up", "device_type": "Display",    "room_sensitivity": "Low"},
        {"name": "Office Display",        "ip": "192.168.1.13", "status": "up", "device_type": "Display",    "room_sensitivity": "Low"},
    ]

# ── Evaluate risk for each host ───────────────────────────────────────────────
rows = []
for h in st.session_state.hosts:
    result = evaluate_risk(h["name"], h["device_type"], h["room_sensitivity"])
    rows.append({
        "Severity":    result["risk_score"],
        "Device":      h["name"],
        "IP":          h["ip"],
        "Issue":       result["recommendation"],
        "RMF Control": result["rmf_control"],
    })

df = pd.DataFrame(rows)

# ── Layout ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([0.7, 0.3])

with col1:
    st.header("Priority Risk List")
    st.dataframe(df, use_container_width=True)

with col2:
    st.header("Compliance Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Ask me about any risk in the table."}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask about a risk..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Match question to a row in the table
        match = df[df["Device"].str.contains(prompt, case=False) |
                   df["Issue"].str.contains(prompt, case=False)]
        if not match.empty:
            row = match.iloc[0]
            reply = f"**{row['Device']}** — {row['Severity']}\n\n{row['Issue']}\n\nRMF Control: `{row['RMF Control']}`"
        else:
            reply = "No matching device found. Try typing a device name or issue keyword."

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
