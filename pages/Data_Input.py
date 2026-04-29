import os

import pandas as pd
import streamlit as st
from supabase import create_client

# -------------------------
# CONFIG
# -------------------------
SCORE_OPTIONS = list(range(0, 11))

AGE_GROUPS = ["U9", "U10", "U11", "U12", "U13", "U14", "U15", "U16", "U18", "Dev"]

DISPLAY_COLUMNS = [
    "id",
    "Age Group",
    "Player",
    "Date",
    "Technical",
    "Physical",
    "Competence",
    "Potential",
    "Comment",
]

# -------------------------
# SUPABASE CONNECTION
# -------------------------
SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error(
        "Supabase credentials are missing. Add SUPABASE_URL and SUPABASE_KEY in "
        ".streamlit/secrets.toml or as environment variables."
    )
    st.stop()

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as exc:
    st.error(f"Failed to initialize Supabase client: {exc}")
    st.stop()

# -------------------------
# PAGE TITLE
# -------------------------
st.title("Manual Data Entry")

# -------------------------
# LOAD DATA FROM SUPABASE
# -------------------------
try:
    response = supabase.table("player_records").select("*").execute()
    data = response.data
except Exception as exc:
    st.error(f"Could not read from Supabase table 'player_records': {exc}")
    st.stop()

df = pd.DataFrame(data)

if not df.empty:
    df = df.rename(columns={
        "age_group": "Age Group",
        "player": "Player",
        "date": "Date",
        "technical": "Technical",
        "physical": "Physical",
        "competence": "Competence",
        "potential": "Potential",
        "comment": "Comment",
    })

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

# -------------------------
# ENTRY FORM
# -------------------------
with st.form("entry_form"):
    age_group = st.selectbox("Age Group", AGE_GROUPS)
    player = st.text_input("Player Name")
    date = st.date_input("Date")

    technical = st.select_slider("Technical", options=SCORE_OPTIONS, value=0)
    physical = st.select_slider("Physical", options=SCORE_OPTIONS, value=0)
    competence = st.select_slider("Competence", options=SCORE_OPTIONS, value=0)
    potential = st.select_slider("Potential", options=SCORE_OPTIONS, value=0)

    comment = st.text_area("Action Points")

    submit = st.form_submit_button("Save Entry")

# -------------------------
# SAVE NEW ENTRY
# -------------------------
if submit:
    new_row = {
        "age_group": age_group,
        "player": player,
        "date": str(date),
        "technical": technical,
        "physical": physical,
        "competence": competence,
        "potential": potential,
        "comment": comment,
    }

    try:
        supabase.table("player_records").insert(new_row).execute()
    except Exception as exc:
        st.error(f"Failed to save entry to Supabase: {exc}")
        st.stop()

    st.success("Entry saved")
    st.rerun()  # refresh data instantly

# -------------------------
# DISPLAY + EDIT DATA
# -------------------------
st.subheader("Raw Saved Data")

if df.empty:
    st.info("No entries saved yet.")
else:
    edited_df = st.data_editor(
        df[DISPLAY_COLUMNS],
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Age Group": st.column_config.SelectboxColumn("Age Group", options=AGE_GROUPS),
            "Technical": st.column_config.SelectboxColumn("Technical", options=SCORE_OPTIONS),
            "Physical": st.column_config.SelectboxColumn("Physical", options=SCORE_OPTIONS),
            "Competence": st.column_config.SelectboxColumn("Competence", options=SCORE_OPTIONS),
            "Potential": st.column_config.SelectboxColumn("Potential", options=SCORE_OPTIONS),
        },
        key="raw_data_editor",
    )

    # -------------------------
    # SAVE EDITED DATA
    # -------------------------
    if st.button("Save Table Changes"):
        for _, row in edited_df.iterrows():
            try:
                supabase.table("player_records").update({
                    "age_group": row["Age Group"],
                    "player": row["Player"],
                    "date": str(row["Date"]),
                    "technical": int(row["Technical"]),
                    "physical": int(row["Physical"]),
                    "competence": int(row["Competence"]),
                    "potential": int(row["Potential"]),
                    "comment": row["Comment"],
                }).eq("id", int(row["id"])).execute()
            except Exception as exc:
                st.error(f"Failed to update row id={int(row['id'])}: {exc}")
                st.stop()

        st.success("Data updated")
        st.rerun()
