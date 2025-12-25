
# Q1:
# Create a Streamlit application that allows users to upload a CSV file and view its schema.Use an LLM to convert user questions into SQL queries, execute them on the CSV data using pandasql, and explain the results in simple English.


import streamlit as st
import pandas as pd
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pandasql import sqldf
import os

load_dotenv()

st.title("Ask CSV using SQL (Groq)")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("CSV Schema")
    st.write(df.dtypes)

    question = st.text_input("Ask anything about this CSV:")

    if question:
        prompt = f"""
        Table Name: data
        Table Schema: {df.dtypes}

        Question: {question}

        Instruction:
        Write ONLY a valid SQLite SQL query.
        Do NOT use markdown or ```sql blocks.
        Do not explain anything.
        """

        result = llm.invoke(prompt)

        sql_query = result.content.strip()

        #  Removing markdown SQL blocks if LLM adds it
        if sql_query.startswith("```"):
            sql_query = "\n".join(sql_query.splitlines()[1:-1]).strip()

        st.subheader("Generated SQL")
        st.code(sql_query, language="sql")

        try:
            query_result = sqldf(sql_query, {"data": df})
            st.subheader("Query Result")
            st.dataframe(query_result)

            explanation_prompt = f"""
            Here is the result of a SQL query executed on a table:
            {query_result}

            Explain the result in plain English in short.
            """

            explanation = llm.invoke(explanation_prompt)
            st.subheader("Explanation")
            st.write(explanation.content.strip())

        except Exception as e:
            st.error(f"SQL Execution Error: {e}")
