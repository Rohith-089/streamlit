import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Title
st.title("📋 Attendance Tracker")

# Initialize session state
if "students" not in st.session_state:
    st.session_state.students = []

if "attendance" not in st.session_state:
    st.session_state.attendance = {}

# Add a new student
with st.form("add_student_form"):
    new_student = st.text_input("Enter student name")
    submitted = st.form_submit_button("➕ Add Student")
    if submitted and new_student:
        if new_student not in st.session_state.students:
            st.session_state.students.append(new_student)
            st.success(f"{new_student} added successfully.")
        else:
            st.warning("Student already exists.")

# Display attendance sheet
st.subheader("🗓️ Mark Attendance")
today = datetime.now().strftime("%Y-%m-%d")
if today not in st.session_state.attendance:
    st.session_state.attendance[today] = {}

# Form for attendance
with st.form("attendance_form"):
    for student in st.session_state.students:
        present = st.checkbox(f"{student}", key=student)
        st.session_state.attendance[today][student] = "Present" if present else "Absent"

    submit_attendance = st.form_submit_button("✅ Submit Attendance")

if submit_attendance:
    st.success("Attendance submitted successfully.")

# Display today's attendance
st.subheader("📊 Today's Attendance")
if today in st.session_state.attendance:
    df_today = pd.DataFrame.from_dict(st.session_state.attendance[today], orient="index", columns=["Status"])
    df_today.index.name = "Student Name"
    st.dataframe(df_today)

# Export attendance
st.subheader("📁 Export Data")
if st.button("⬇️ Download Today's Attendance as CSV"):
    if df_today is not None:
        csv = df_today.to_csv().encode('utf-8')
        st.download_button("Download CSV", csv, f"attendance_{today}.csv", "text/csv")
    else:
        st.warning("No attendance data available.")

# Display full history
if st.checkbox("📚 Show Full Attendance History"):
    all_days = []
    for date, records in st.session_state.attendance.items():
        df = pd.DataFrame.from_dict(records, orient="index", columns=["Status"])
        df["Date"] = date
        df["Student Name"] = df.index
        all_days.append(df)

    if all_days:
        full_df = pd.concat(all_days)
        st.dataframe(full_df[["Date", "Student Name", "Status"]].reset_index(drop=True))
