import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/dataset.csv")

st.title("Dashboard")

department_filter = st.multiselect(
    "Filter by Department",
    df["Department"].unique(),
    default=df["Department"].unique()
)

filtered_df = df[df["Department"].isin(department_filter)]

st.dataframe(filtered_df)

fig = px.histogram(filtered_df, x="Department")
st.plotly_chart(fig, use_container_width=True)
