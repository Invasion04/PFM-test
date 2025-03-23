import streamlit as st
import requests

# Backend API URL (Change this if needed)
API_URL = "http://127.0.0.1:5000"

# Streamlit Page Title
st.title("💰 Personal Finance Manager")

# Home Message
st.write("Manage your expenses with Firebase and Flask API")

# Fetch Expenses from API
st.subheader("📋 Expense List")
if st.button("Load Expenses"):
    response = requests.get(f"{API_URL}/get_expenses")
    if response.status_code == 200:
        expenses = response.json()
        for expense in expenses:
            st.write(f"**{expense.get('name', 'Unknown')}** - ${expense.get('amount', 0)}")
    else:
        st.error("Failed to fetch expenses")

# Add Expense
st.subheader("➕ Add Expense")
expense_name = st.text_input("Expense Name")
expense_amount = st.number_input("Amount", min_value=0.0)
if st.button("Add Expense"):
    data = {"name": expense_name, "amount": expense_amount}
    response = requests.post(f"{API_URL}/add_expense", json=data)
    if response.status_code == 201:
        st.success("Expense added successfully!")
    else:
        st.error("Failed to add expense")

# Delete Expense
st.subheader("❌ Delete Expense")
expense_id = st.text_input("Expense ID to delete")
if st.button("Delete Expense"):
    response = requests.delete(f"{API_URL}/delete_expense/{expense_id}")
    if response.status_code == 200:
        st.success("Expense deleted successfully!")
    else:
        st.error("Failed to delete expense")

