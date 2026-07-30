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

with st.sidebar:
    st.header("➕ Add Expense")

    amount = st.number_input(
        "Amount",
        min_value=0.0
    )

    category = st.text_input(
        "Category"
    )

    description = st.text_input(
        "Description"
    )

    date = st.date_input(
        "Date"
    )

    add_button = st.button(
        "Add Expense"
    )

if add_button:
    expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": str(date)
    }

    st.session_state.expenses.append(expense)
    
    save_expenses(st.session_state.expenses)

    st.success("Expense added!")

st.subheader("📋 Expense History")

for index, expense in enumerate(st.session_state.expenses):

    with st.container():

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(expense["date"])

        with col2:
            st.write(expense["category"])

        with col3:
            st.write(f"RM {expense['amount']:.2f}")

        st.write(expense["description"])

        edit_col, delete_col = st.columns(2)

        with edit_col:
            if st.button(
                "✏️ Edit",
                key=f"edit_{index}"
            ):
                st.session_state.editing = index
                st.rerun()
        
        with delete_col:
            if st.button(
                "🗑️ Delete",
                key=f"delete_{index}"
            ):
                st.session_state.expenses.pop(index)
                save_expenses(st.session_state.expenses)
                st.rerun()

        st.divider()

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
            expense.get("date", str(datetime.today().date())),
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

expense_count = len(st.session_state.expenses)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Spent",
        f"RM {total:.2f}"
    )

with col2:
    st.metric(
        "Number of Expenses",
        expense_count
    )
