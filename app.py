import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Dynamic Cell Tracker", layout="wide")

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 1. Load Members (from the "ROSTER" tab)
df_members = conn.read(worksheet="ROSTER", ttl="0")
# Clean up any empty rows parsed from Sheets
df_members = df_members.dropna(subset=['Name'])
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

    # ADD MEMBER LOGIC WITH FIXED INDENTATION
    if st.button("Add to List"):
        if new_name and new_name not in all_members:
            new_row = pd.DataFrame([{"Name": new_name}])
            updated_df = pd.concat([df_members, new_row], ignore_index=True)

            # Writes specifically to the "ROSTER" tab
            conn.update(worksheet="ROSTER", data=updated_df)

            st.success(f"Added {new_name}!")
            st.rerun()
        elif new_name in all_members:
            st.warning("Member already exists!")

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
        # Create the history rows (Columns map exactly to your screenshot)
        history_entry = pd.DataFrame({
            "Date": [str(meeting_date)] * len(attendance_data),
            "Meeting Name": [meeting_name] * len(attendance_data),
            "Attendance": attendance_data
        })

        # Load existing history, add new data, and save back to "HISTORY" tab
        df_history = conn.read(worksheet="HISTORY", ttl="0")
        updated_history = pd.concat([df_history, history_entry], ignore_index=True)
        conn.update(worksheet="HISTORY", data=updated_history)

        st.success(f"Successfully saved {len(attendance_data)} records to Google Sheets History!")
        st.balloons()
    else:
        st.error("Please select at least one person.")
