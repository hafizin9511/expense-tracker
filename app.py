import streamlit as st

st.title("💰 Expense Tracker")

if "expenses" not in st.session_state:
    st.session_state.expenses = []

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

    st.session_state.expenses.append(expense)

    st.success("Expense added!")

st.subheader("📋 Your Expenses")

for expense in st.session_state.expenses:
    st.write(
        f"""
        **Date:** {expense['date']}  
        **Category:** {expense['category']}  
        **Description:** {expense['description']}  
        **Amount:** ${expense['amount']:.2f}
        """
    )
