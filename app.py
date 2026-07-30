import streamlit as st

st.title("💰 Expense Tracker")

expenses = []

amount = st.number_input("Amount", min_value=0.0)

category = st.text_input("Category")

description = st.text_input("Description")

date = st.date_input("Date")

if st.button("Add Expense"):
    expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": str(date)
    }

    expenses.append(expense)

    st.success("Expense added!")

st.write(expenses)
