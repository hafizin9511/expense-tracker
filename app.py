import streamlit as st
import sqlite3
import pandas as pd
import uuid
from datetime import datetime

st.set_page_config(page_title="Expense Tracker", page_icon="💰")


# ---------------- DATABASE ---------------- #

@st.cache_resource
def get_connection():
    conn = sqlite3.connect("expenses.db", check_same_thread=False)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id TEXT PRIMARY KEY,
            amount REAL,
            category TEXT,
            description TEXT,
            date TEXT
        )
    """)
    conn.commit()
    return conn


conn = get_connection()
cursor = conn.cursor()


def load_expenses():
    cursor.execute("""
        SELECT id, amount, category, description, date
        FROM expenses
        ORDER BY date DESC
    """)
    rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "amount": row[1],
            "category": row[2],
            "description": row[3],
            "date": row[4],
        }
        for row in rows
    ]


expenses = load_expenses()

# ---------------- TITLE ---------------- #

st.title("💰 Expense Tracker")

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.header("➕ Add Expense")

    with st.form("expense_form", clear_on_submit=True, enter_to_submit=False):

        amount = st.number_input(
            "Amount",
            min_value=0.0
        )

        category = st.text_input("Category")

        description = st.text_input("Description")

        date = st.date_input("Date")

        submitted = st.form_submit_button("Add Expense")

    if submitted:

        if category.strip() == "":
            st.error("Please enter a category.")
        else:
            cursor.execute("""
                INSERT INTO expenses
                (id, amount, category, description, date)
                VALUES (?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()),
                amount,
                category,
                description,
                str(date)
            ))

            conn.commit()
            st.success("Expense added!")
            st.rerun()

    st.divider()

    st.header("🔍 Filter")

    categories = ["All"] + sorted(
        list(set(exp["category"] for exp in expenses))
    )

    selected_category = st.selectbox(
        "Category",
        categories
    )

    st.divider()

    if st.button("🗑 Reset Data"):
        cursor.execute("DELETE FROM expenses")
        conn.commit()
        st.rerun()

# ---------------- FILTER ---------------- #

if selected_category == "All":
    filtered_expenses = expenses
else:
    filtered_expenses = [
        e for e in expenses
        if e["category"] == selected_category
    ]

# ---------------- HISTORY ---------------- #

st.subheader("📋 Expense History")

for index, expense in enumerate(filtered_expenses):

    with st.container():

        c1, c2, c3 = st.columns(3)

        c1.write(expense["date"])
        c2.write(expense["category"])
        c3.write(f"RM {expense['amount']:.2f}")

        st.write(expense["description"])

        edit_col, delete_col = st.columns(2)

        with edit_col:

            if st.button(
                "✏️ Edit",
                key=f"edit_{expense['id']}"
            ):
                st.session_state.editing = expense["id"]
                st.rerun()

        with delete_col:

            if st.button(
                "🗑️ Delete",
                key=f"delete_{expense['id']}"
            ):
                cursor.execute(
                    "DELETE FROM expenses WHERE id=?",
                    (expense["id"],)
                )

                conn.commit()
                st.rerun()

        st.divider()

# ---------------- EDIT ---------------- #

if "editing" in st.session_state:

    expense = next(
        (
            e for e in expenses
            if e["id"] == st.session_state.editing
        ),
        None
    )

    if expense:

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

        col1, col2 = st.columns(2)

        with col1:

            if st.button("Save Changes"):

                cursor.execute("""
                    UPDATE expenses
                    SET amount=?,
                        category=?,
                        description=?,
                        date=?
                    WHERE id=?
                """, (
                    new_amount,
                    new_category,
                    new_description,
                    str(new_date),
                    expense["id"]
                ))

                conn.commit()

                del st.session_state.editing

                st.success("Expense updated!")

                st.rerun()

        with col2:

            if st.button("Cancel"):
                del st.session_state.editing
                st.rerun()

# ---------------- SUMMARY ---------------- #

st.subheader("💰 Summary")

total = sum(e["amount"] for e in expenses)

count = len(expenses)

c1, c2 = st.columns(2)

c1.metric("Total Spent", f"RM {total:.2f}")
c2.metric("Number of Expenses", count)

# ---------------- CHART ---------------- #

st.subheader("📊 Spending by Category")

if expenses:

    df = pd.DataFrame(expenses)

    chart = (
        df.groupby("category")["amount"]
        .sum()
    )

    st.bar_chart(chart)

else:

    st.info("No expenses available.")
