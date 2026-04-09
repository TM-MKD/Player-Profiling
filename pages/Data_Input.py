import streamlit as st
import pandas as pd
import os

FILE_PATH = "data/records.csv"

st.title("Manual Data Entry")

# Load data
if os.path.exists(FILE_PATH):
    df = pd.read_csv(FILE_PATH)
else:
    df = pd.DataFrame(columns=[
        "Coach",
        "Date",
        "Category",
        "Score",
        "Comment"
    ])

with st.form("entry_form"):
    coach = st.text_input("Coach Name")
    date = st.date_input("Date")
    category = st.selectbox(
        "Category",
        ["Understanding Self", "Coaching Individuals", "Session Design"]
    )
    score = st.slider("Score", 1, 5)
    comment = st.text_area("Comment")

    submit = st.form_submit_button("Save Entry")

if submit:
    new_row = pd.DataFrame([{
        "Coach": coach,
        "Date": date,
        "Category": category,
        "Score": score,
        "Comment": comment
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)

    st.success("Entry saved")
