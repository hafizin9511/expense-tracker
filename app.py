import streamlit as st
import json
from datetime import datetime

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

for index, expense in enumerate(st.session_state.expenses):

    st.write(
        f"""
        **Date:** {expense['date']}  
        **Category:** {expense['category']}  
        **Description:** {expense['description']}  
        **Amount:** RM {expense['amount']:.2f}
        """
    )

    if st.button("✏️ Edit", key=f"edit_{index}"):
        st.session_state.editing = index

    if st.button("🗑️ Delete", key=index):
        st.session_state.expenses.pop(index)
        save_expenses(st.session_state.expenses)
        st.rerun()

if "editing" in st.session_state:

    index = st.session_state.editing
    expense = st.session_state.expenses[index]

    st.subheader("✏️ Edit Expense")

    new_amount = st.number_input(
        "Amount",
        value=float(expense["amount"])
    )

    new_category = st.text_input(
        "Category",
        value=expense["category"]
    )

    new_description = st.text_input(
        "Description",
        value=expense["description"]
    )

    new_date = st.date_input(
        "Date",
        value=datetime.strptime(
            expense["date"],
            "%Y-%m-%d"
        )
    )

    if st.button("Save Changes"):

        expense["amount"] = new_amount
        expense["category"] = new_category
        expense["description"] = new_description
        expense["date"] = str(new_date)

        save_expenses(st.session_state.expenses)

        del st.session_state.editing

        st.success("Expense updated!")

        st.rerun()
        
st.subheader("💰 Summary")

total = sum(
    expense["amount"]
    for expense in st.session_state.expenses
)

st.metric(
    "Total Spent",
    f"RM {total:.2f}"
)
