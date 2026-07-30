import streamlit as st

st.title("💰 Expense Tracker")

amount = st.number_input("Amount", min_value=0.0)

category = st.text_input("Category")

description = st.text_input("Description")

date = st.date_input("Date")

if st.button("Add Expense"):
    st.success("Expense added!")
