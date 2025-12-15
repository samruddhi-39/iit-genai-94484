# 1.
# Upload a CSV file. Input a SQL query from user and execute it on the CSV
# data (as dataframe ). Display result on the

import streamlit as st
import pandas as pd
from pandasql import sqldf

st.title("SQL on Data")

# Upload CSV file
uploaded_file = st.file_uploader("Upload CSV file here :", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("CSV Data Preview")
    st.dataframe(df)

    st.markdown("### Write SQL Query")
    st.write("Use table name as **df**")

    query = st.text_area(
        "Example: SELECT * FROM df LIMIT 5"
    )

    if st.button("Run Query"):
        try:
            result = sqldf(query)
            st.subheader("Query Result")
            st.dataframe(result)
        except Exception as e:
            st.error(f"Error: {e}")
