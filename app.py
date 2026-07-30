import streamlit as st
import json

def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)
        
st.title("💰 Expense Tracker")

if "expenses" not in st.session_state:
    st.session_state.expenses = load_expenses()

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
    
    save_expenses(st.session_state.expenses)

    st.success("Expense added!")

st.subheader("📋 Your Expenses")

for expense in st.session_state.expenses:
    st.write(
        f"""
        **Date:** {expense['date']}  
        **Category:** {expense['category']}  
        **Description:** {expense['description']}  
        **Amount:** RM {expense['amount']:.2f}
        """
    )

st.subheader("💰 Summary")

total = sum(
    expense["amount"]
    for expense in st.session_state.expenses
)

st.metric(
    "Total Spent",
    f"RM {total:.2f}"
)
