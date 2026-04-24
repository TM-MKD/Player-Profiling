import os

import pandas as pd
import streamlit as st

FILE_PATH = "data/records.csv"

st.title("Dashboard")

if not os.path.exists(FILE_PATH):
    st.info("No data found yet. Save entries in the Data Entry page to populate the dashboard.")
    st.stop()

df = pd.read_csv(FILE_PATH)

if df.empty:
    st.info("No records available yet. Add data in the Data Entry page.")
    st.stop()

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

