import streamlit as st
import pandas as pd

# 1. Page Config
st.set_page_config(layout="wide", page_title="AV-Sec Architect")
st.title("🛡️ AV-Sec Architect: Compliance Dashboard")

# 2. Layout: Split screen into 2 columns
col1, col2 = st.columns([0.7, 0.3])

with col1:
    st.header("Priority Risk List")
    
    # Example data (In a real app, this comes from your Nmap scanner)
    data = {
        "Severity": ["🔴 High", "🟡 Medium", "🟢 Low"],
        "Device": ["Boardroom Mic (Sony)", "Lobby Camera (Axis)", "Office Display"],
        "Issue": ["Unencrypted Stream", "Default Password", "Firmware Update"],
        "RMF Control": ["AC-2", "IA-5", "SI-2"]
    }
    df = pd.DataFrame(data)
    
    # Displaying the list (Your Choice #2)
    st.table(df)

with col2:
    st.header("Compliance Assistant")
    
    # Initialize chat history (The Chat Box you chose)
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How can I help you fix these risks?"}]

    # Display chat messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # User Input
    if prompt := st.chat_input("Ask about a risk..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Simple AI Logic (This is the 'blank' I fill in later)
        response = f"I see you're asking about '{prompt}'. Should I pull the manual for that device?"
        st.chat_message("assistant").write(response)
