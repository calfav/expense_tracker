import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def analytics_months_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1), key="month_start")

    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 31), key="month_end")

    if st.button("Get Monthly Analytics", key="get_monthly_btn"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        response = requests.post(f"{API_URL}/analytics_by_month/", json=payload)
        response = response.json()

        data = {
            "Month": list(response.keys()),
            "Total": [response[month]["total"] for month in response]
        }

        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by="Month")

        st.title("Expense Breakdown By Month")

        st.bar_chart(data=df_sorted.set_index("Month")["Total"], use_container_width=True)

        df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
        st.table(df_sorted)
