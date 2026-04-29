import os

import pandas as pd
import streamlit as st

FILE_PATH = "data/records.csv"
SCORE_OPTIONS = list(range(0, 11))
COLUMNS = [
    "Age Group",
    "Player",
    "Month",
    "Technical",
    "Physical",
    "Competence",
    "Potential",
    "Comment",
]

st.title("Manual Data Entry")

# Load data
if os.path.exists(FILE_PATH):
    df = pd.read_csv(FILE_PATH)
else:
    df = pd.DataFrame(columns=COLUMNS)

with st.form("entry_form"):
    age_group = st.selectbox(
        "Age Group",
        ["U9", "U10", "U11", "U12", "U13", "U14", "U15", "U16", "U18", "Dev"],
    )
    player = st.text_input("Player Name")
    month = st.selectbox(
        "Month",
        ["August", "September", "October", "November", "December", "January", "February", "March", "April"],
    )
    technical = st.select_slider("Technical", options=SCORE_OPTIONS, value=0)
    physical = st.select_slider("Physical", options=SCORE_OPTIONS, value=0)
    competence = st.select_slider("Competence", options=SCORE_OPTIONS, value=0)
    potential = st.select_slider("Potential", options=SCORE_OPTIONS, value=0)

    comment = st.text_area("Action Points")
    submit = st.form_submit_button("Save Entry")

if submit:
    new_row = pd.DataFrame(
        [
            {
                "Age Group": age_group,
                "Player": player,
                "Month": month,
                "Technical": technical,
                "Physical": physical,
                "Competence": competence,
                "Potential": potential,
                "Comment": comment,
            }
        ]
    )

    df = pd.concat([df, new_row], ignore_index=True)

    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    df.to_csv(FILE_PATH, index=False)

    st.success("Entry saved")

st.subheader("Raw Saved Data")
if df.empty:
    st.info("No entries saved yet.")
else:
    editable_df = df.copy()
    if "Date" in editable_df.columns:
        editable_df["Date"] = pd.to_datetime(editable_df["Date"], errors="coerce").dt.date

    edited_df = st.data_editor(
        editable_df,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Age Group": st.column_config.SelectboxColumn(
                "Age Group",
                options=["U9", "U10", "U11", "U12", "U13", "U14", "U15", "U16", "U18", "Dev"],
            ),
            "Technical": st.column_config.SelectboxColumn("Technical", options=SCORE_OPTIONS),
            "Physical": st.column_config.SelectboxColumn("Physical", options=SCORE_OPTIONS),
            "Competence": st.column_config.SelectboxColumn("Competence", options=SCORE_OPTIONS),
            "Potential": st.column_config.SelectboxColumn("Potential", options=SCORE_OPTIONS),
        },
        key="raw_data_editor",
    )

    if st.button("Save Table Changes"):
        if "Date" in edited_df.columns:
            edited_df["Date"] = pd.to_datetime(edited_df["Date"], errors="coerce").dt.date

        edited_df = edited_df.reindex(columns=COLUMNS)
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
        edited_df.to_csv(FILE_PATH, index=False)
        st.success("Raw saved data updated")
