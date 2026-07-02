import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Professional Page Config
st.set_page_config(page_title="Team Operations Tracker", layout="wide")

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. SRE Upgrade: Try/Except Block for Database Reads
try:
    df_members = conn.read(worksheet="ROSTER", ttl="0")
    df_members = df_members.dropna(subset=['Name'])
    all_members = df_members['Name'].tolist()
except Exception as e:
    st.error("⚠️ Critical Error: Unable to connect to the cloud database. Please check your connection.")
    st.stop() # Stops the app gracefully instead of crashing with a massive red error log

st.title("📊 Team Operations & Attendance Tracker")

# --- SIDEBAR: ADMIN CONTROLS ---
with st.sidebar:
    st.header("⚙️ Shift Settings")
    meeting_name = st.text_input("Event/Shift Name", "Daily Shift Sync")
    meeting_date = st.date_input("Date", datetime.now())

    st.divider()
    st.header("➕ Add New Member")
    new_name = st.text_input("Full Name")

    if st.button("Add to Roster"):
        if new_name and new_name not in all_members:
            try:
                new_row = pd.DataFrame([{"Name": new_name}])
                updated_df = pd.concat([df_members, new_row], ignore_index=True)
                conn.update(worksheet="ROSTER", data=updated_df)
                st.success(f"Added {new_name} to the roster!")
                st.rerun()
            except Exception as e:
                st.error("Failed to update roster. Try again later.")
        elif new_name in all_members:
            st.warning("Member already exists in the roster!")

# --- MAIN AREA: DASHBOARD METRICS ---
st.markdown(f"**Total Registered Team Members:** `{len(all_members)}`")
st.divider()

search_query = st.text_input("🔍 Search Roster...", "")
filtered_members = [m for m in all_members if search_query.lower() in str(m).lower()]

attendance_data = []
if filtered_members:
    cols = st.columns(3)
    for i, member in enumerate(filtered_members):
        with cols[i % 3]:
            if st.checkbox(member, key=member):
                attendance_data.append(member)

st.divider()

# --- ISOLATED SUBMIT ACTION WITH DYNAMIC FEEDBACK ---
if len(attendance_data) > 0:
    st.info(f"📌 You are about to log attendance for **{len(attendance_data)}** team members for the **{meeting_name}**.")
else:
    st.info("📌 Select team members above to enable submission.")

# The button is now disabled until at least one person is selected
if st.button("Submit & Save to History", type="primary", disabled=len(attendance_data) == 0):
    try:
        history_entry = pd.DataFrame({
            "Date": [str(meeting_date)] * len(attendance_data),
            "Meeting Name": [meeting_name] * len(attendance_data),
            "Attendance": attendance_data
        })

        df_history = conn.read(worksheet="HISTORY", ttl="0")
        updated_history = pd.concat([df_history, history_entry], ignore_index=True)
        conn.update(worksheet="HISTORY", data=updated_history)

        st.success(f"✅ Successfully saved {len(attendance_data)} records to the cloud database!")
        st.balloons()
    except Exception as e:
        st.error("🚨 Critical Error: Could not write to the database. Please try again.")
