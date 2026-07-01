import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Dynamic Cell Tracker", layout="wide")

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 1. Load Members (from Sheet1)
df_members = conn.read(worksheet="Sheet1", ttl="0")
all_members = df_members['Name'].tolist()

st.title("📊 Attendance & History Tracker")

# --- SIDEBAR: ADD NEW MEMBERS ---
with st.sidebar:
    st.header("Meeting Settings")
    meeting_name = st.text_input("Meeting Name", "Dynamic Cell")
    meeting_date = st.date_input("Date", datetime.now())
    
    st.divider()
    st.header("Add New Member")
    new_name = st.text_input("Full Name")
    if st.button("Add to List"):
        if new_name and new_name not in all_members:
            new_row = pd.DataFrame([{"Name": new_name}])
            updated_df = pd.concat([df_members, new_row], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
            st.success(f"Added {new_name}!")
            st.rerun()

# --- MAIN AREA: ATTENDANCE ---
search_query = st.text_input("🔍 Search Members...", "")
filtered_members = [m for m in all_members if search_query.lower() in str(m).lower()]

attendance_data = []
if filtered_members:
    cols = st.columns(3)
    for i, member in enumerate(filtered_members):
        with cols[i % 3]:
            if st.checkbox(member, key=member):
                attendance_data.append(member)

# --- SUBMIT TO HISTORY ---
if st.button("Submit & Save to History", type="primary"):
    if attendance_data:
        # Create the history rows
        history_entry = pd.DataFrame({
            "Date": [str(meeting_date)] * len(attendance_data),
            "Meeting Name": [meeting_name] * len(attendance_data),
            "Attendee": attendance_data
        })
        
        # Load existing history, add new data, and save back to "History" tab
        df_history = conn.read(worksheet="History", ttl="0")
        updated_history = pd.concat([df_history, history_entry], ignore_index=True)
        conn.update(worksheet="History", data=updated_history)
        
        st.success(f"Successfully saved {len(attendance_data)} records to Google Sheets History!")
        st.balloons() # Celebration!
    else:
        st.error("Please select at least one person.")
