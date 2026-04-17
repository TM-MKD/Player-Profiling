import os

import pandas as pd
import streamlit as st

FILE_PATH = "data/records.csv"
SCORE_OPTIONS = list(range(0, 11))

st.title("Manual Data Entry")

# Load data
if os.path.exists(FILE_PATH):
    df = pd.read_csv(FILE_PATH)
else:
    df = pd.DataFrame(columns=[
        "Age Group",
        "Player",
        "Date",
        "Technical",
        "Physical",
        "Competence",
        "Potential",
        "Comment",
    ])

with st.form("entry_form"):
    age_group = st.selectbox(
        "Age Group",
        ["U9", "U10", "U11", "U12", "U13", "U14", "U15", "U16", "U18", "Dev"],
    )
    player = st.text_input("Player Name")
    date = st.date_input("Date")

    technical = st.select_slider("Technical", options=SCORE_OPTIONS, value=5)
    physical = st.select_slider("Physical", options=SCORE_OPTIONS, value=5)
    competence = st.select_slider("Competence", options=SCORE_OPTIONS, value=5)
    potential = st.select_slider("Potential", options=SCORE_OPTIONS, value=5)

    comment = st.text_area("Action Points")
    submit = st.form_submit_button("Save Entry")

if submit:
    new_row = pd.DataFrame([
        {
            "Age Group": age_group,
            "Player": player,
            "Date": date,
            "Technical": technical,
            "Physical": physical,
            "Competence": competence,
            "Potential": potential,
            "Comment": comment,
        }
    ])

    df = pd.concat([df, new_row], ignore_index=True)

    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    df.to_csv(FILE_PATH, index=False)

    st.success("Entry saved")
