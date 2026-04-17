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
        "Player",
        "Date",
        "Category",
        "Score",
        "Comment"
    ])

with st.form("entry_form"):
    player = st.text_input("Player Name")
    date = st.date_input("Date")
    category = st.selectbox(
        "Category",
        ["Technical", "Physical", "Competence", "Potential"]
    )
    score = st.slider("Score", 0, 10)
    comment = st.text_area("Action Points")

    submit = st.form_submit_button("Save Entry")

if submit:
    new_row = pd.DataFrame([{
        "Player": player,
        "Date": date,
        "Category": category,
        "Score": score,
        "Comment": comment
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    df.to_csv(FILE_PATH, index=False)

    st.success("Entry saved")
