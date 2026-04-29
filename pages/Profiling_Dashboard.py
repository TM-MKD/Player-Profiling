import os

import pandas as pd
import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

st.title("Dashboard")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error(
        "Supabase credentials are missing. Add SUPABASE_URL and SUPABASE_KEY in "
        ".streamlit/secrets.toml or as environment variables."
    )
    st.stop()

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    response = supabase.table("player_records").select("*").execute()
    df = pd.DataFrame(response.data)
except Exception as exc:
    st.error(f"Could not load data from Supabase table 'player_records': {exc}")
    st.stop()

if df.empty:
    st.info("No records available yet. Add data in the Data Entry page.")
    st.stop()

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

if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

age_groups = sorted(df["Age Group"].dropna().unique().tolist())
selected_age_groups = st.multiselect(
    "Filter by Age Group",
    age_groups,
    default=age_groups,
)

players = sorted(df["Player"].dropna().unique().tolist())
selected_players = st.multiselect(
    "Filter by Player",
    players,
    default=players,
)

filtered_df = df[
    df["Age Group"].isin(selected_age_groups)
    & df["Player"].isin(selected_players)
]

st.subheader("Filtered Records")
st.dataframe(filtered_df, use_container_width=True)

metric_options = ["Technical", "Physical", "Competence", "Potential"]
selected_metric = st.selectbox("Metric", metric_options)

avg_scores = (
    filtered_df.groupby("Player", dropna=False)[selected_metric]
    .mean()
    .reset_index()
    .sort_values(selected_metric, ascending=False)
)

st.subheader(f"Average {selected_metric} by Player")
if avg_scores.empty:
    st.info("No data available for the selected filters.")
else:
    chart_df = avg_scores.set_index("Player")
    st.bar_chart(chart_df[selected_metric], use_container_width=True)
