import streamlit as st

st.set_page_config(
    page_title="MK Dons – Coach Analytics Hub",
    layout="wide"
)

st.title("MK Dons – Coach Analytics Hub")

col1, col2 = st.columns(2)

with col1:
    st.info("Use the Data Entry page to manually record observations.")

with col2:
    st.success("Use the Dashboard page to analyse live results.")
