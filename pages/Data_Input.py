import os
from urllib.parse import urlparse

import pandas as pd
import streamlit as st
from supabase import Client, create_client


FILE_PATH = "data/records.csv"
SUPABASE_TABLE = st.secrets.get("SUPABASE_TABLE", os.getenv("SUPABASE_TABLE", "player_profiles"))
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


def normalize_supabase_url(raw_url: str | None) -> str | None:
    if not raw_url:
        return None

    cleaned = raw_url.strip().rstrip("/")
    if not cleaned:
        return None

    parsed = urlparse(cleaned)
    if "supabase.com" in parsed.netloc and "/dashboard/project/" in parsed.path:
        project_ref = parsed.path.split("/dashboard/project/", maxsplit=1)[-1].split("/", maxsplit=1)[0]
        if project_ref:
            return f"https://{project_ref}.supabase.co"

    return cleaned


@st.cache_resource(show_spinner=False)
def get_supabase_client() -> Client | None:
    raw_supabase_url = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL"))
    supabase_url = normalize_supabase_url(raw_supabase_url)
    supabase_key = st.secrets.get("SUPABASE_ANON_KEY", os.getenv("SUPABASE_ANON_KEY"))

    if not supabase_url or not supabase_key:
        return None

    return create_client(supabase_url, supabase_key)


def save_to_supabase(row: dict) -> tuple[bool, str]:
    client = get_supabase_client()

    if client is None:
        return (
            False,
            "Supabase not configured. Add SUPABASE_URL and SUPABASE_ANON_KEY to connect cloud storage. "
            "If you pasted a dashboard URL, use the project API URL (https://<project-ref>.supabase.co).",
        )

    payload = {
        "age_group": row["Age Group"],
        "player": row["Player"],
        "month": row["Month"],
        "technical": row["Technical"],
        "physical": row["Physical"],
        "competence": row["Competence"],
        "potential": row["Potential"],
        "comment": row["Comment"],
    }

    try:
        client.table(SUPABASE_TABLE).insert(payload).execute()
        return True, "Saved to Supabase."
    except Exception as exc:
        return False, f"Could not save to Supabase: {exc}"


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
    row = {
        "Age Group": age_group,
        "Player": player,
        "Month": month,
        "Technical": technical,
        "Physical": physical,
        "Competence": competence,
        "Potential": potential,
        "Comment": comment,
    }

    new_row = pd.DataFrame([row])
    df = pd.concat([df, new_row], ignore_index=True)

    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    df.to_csv(FILE_PATH, index=False)

    st.success("Entry saved locally")

    saved_remote, remote_message = save_to_supabase(row)
    if saved_remote:
        st.success(remote_message)
    else:
        st.warning(remote_message)

st.subheader("Raw Saved Data")
if df.empty:
    st.info("No entries saved yet.")
else:
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Age Group": st.column_config.SelectboxColumn(
                "Age Group",
                options=["U9", "U10", "U11", "U12", "U13", "U14", "U15", "U16", "U18", "Dev"],
            ),
            "Month": st.column_config.SelectboxColumn(
                "Month",
                options=["August", "September", "October", "November", "December", "January", "February", "March", "April"],
            ),
            "Technical": st.column_config.SelectboxColumn("Technical", options=SCORE_OPTIONS),
            "Physical": st.column_config.SelectboxColumn("Physical", options=SCORE_OPTIONS),
            "Competence": st.column_config.SelectboxColumn("Competence", options=SCORE_OPTIONS),
            "Potential": st.column_config.SelectboxColumn("Potential", options=SCORE_OPTIONS),
        },
        key="raw_data_editor",
    )

    if st.button("Save Table Changes"):
        edited_df = edited_df.reindex(columns=COLUMNS)
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
        edited_df.to_csv(FILE_PATH, index=False)
        st.success("Raw saved data updated")
