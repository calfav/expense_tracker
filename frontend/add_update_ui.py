import streamlit as st
import requests
from datetime import date

API_URL = "http://localhost:8000"

def add_update_tab():
    # Date picker
    expense_date = st.date_input("Expense Date", date.today(), key="expense_date")

    # Init session container
    if "expenses" not in st.session_state:
        st.session_state.expenses = []

    # Load existing expenses
    if st.button("Load Expenses", key="load_btn"):
        resp = requests.get(f"{API_URL}/expenses/{expense_date}")
        if resp.status_code == 200:
            st.session_state.expenses = resp.json() or []
        else:
            st.session_state.expenses = []
            st.error("Failed to fetch expenses")

    st.subheader("Expenses")

    # Show editable rows
    categories = ["Food", "Shopping", "Entertainment", "Bills", "Other"]
    for i, exp in enumerate(st.session_state.expenses):
        col1, col2, col3, col4 = st.columns([1, 1.5, 3, 0.7])

        with col1:
            st.session_state.expenses[i]["amount"] = st.number_input(
                "Amount", value=float(exp.get("amount", 0.0)), key=f"amount_{i}"
            )

        with col2:
            current_cat = exp.get("category", "Food")
            try:
                idx = categories.index(current_cat)
            except ValueError:
                idx = 0
            st.session_state.expenses[i]["category"] = st.selectbox(
                "Category", categories, index=idx, key=f"cat_{i}"
            )

        with col3:
            st.session_state.expenses[i]["notes"] = st.text_input(
                "Notes", value=exp.get("notes", ""), key=f"notes_{i}"
            )

        with col4:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.expenses.pop(i)
                st.rerun()

    # Add new row
    if st.button("➕ Add Expense"):
        st.session_state.expenses.append(
            {"amount": 0.0, "category": "Food", "notes": ""}
        )
        st.rerun()

    # Save
    if st.button("Save Expenses"):
        payload = [
            {
                "amount": exp["amount"],
                "category": exp["category"],
                "notes": exp["notes"],
            }
            for exp in st.session_state.expenses
            if float(exp.get("amount", 0)) > 0
        ]

        if not payload:
            st.warning("No valid expenses to save.")
            return

        resp = requests.post(
            f"{API_URL}/expenses/{expense_date}",
            json=payload,
        )

        if resp.status_code == 200:
            st.success("Expenses saved successfully!")
            st.session_state.expenses = []  # clear UI
            st.rerun()
        else:
            try:
                detail = resp.json().get("detail", "Unknown error")
            except Exception:
                detail = resp.text
            st.error(f"Failed to save expenses: {detail}")
