# Q1:
# Design and implement a Streamlit-based application consisting of two intelligent agents:
# (1) a CSV Question Answering Agent that allows users to upload a CSV file, display its schema, and answer questions by converting them into SQL queries using pandasql; and
# (2) a Web Scraping Agent that retrieves sunbeam internship and batch information from the Sunbeam website and answers user queries.
# The application should maintain complete chat history.
# All responses must be explained in simple English.

import streamlit as st
import pandas as pd
from pandasql import sqldf
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

st.sidebar.title("Select Agent")
agent_option = st.sidebar.selectbox("Choose an agent", ["CSV Agent", "Sunbeam Web Scraper"])

llm = init_chat_model(
    model="phi-3-mini-4k-instruct",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy_key",
    temperature=0
)


if "csv_chat" not in st.session_state:
    st.session_state.csv_chat = []

if "sunbeam_chat" not in st.session_state:
    st.session_state.sunbeam_chat = []


if agent_option == "CSV Agent":
    st.title("CSV Agent")
    file = st.file_uploader("Upload CSV", type="csv")

    if file:
        df = pd.read_csv(file)
        st.write("Schema")
        st.write(df.dtypes)

        @tool
        def csv_tool(query: str) -> str:
            """
            Executes an SQL query on the uploaded CSV file
            and returns the result as text.
            """
            try:
                return sqldf(query, {"data": df}).to_string(index=False)
            except Exception as e:
                return str(e)

        agent = create_agent(model=llm, tools=[csv_tool])

        user_input = st.text_input("Ask a question about the CSV")

        if st.button("Run CSV Agent") and user_input:
            st.session_state.csv_chat.append(("User", user_input))

           
            sql_prompt = f"""
            Table: data
            Schema: {df.dtypes}
            Convert the question into SQL only.
            Question: {user_input}
            """

            response = agent.invoke({"messages": [{"role": "user", "content": sql_prompt}]})
            sql = response["messages"][-1].content

           
            explain_prompt = f"""
            Explain this SQL query in simple English.
            SQL: {sql}
            """
            response = agent.invoke({"messages": [{"role": "user", "content": explain_prompt}]})
            explanation = response["messages"][-1].content

            st.session_state.csv_chat.append(("Agent", explanation))

            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            st.subheader("Explanation")
            st.write(explanation)

   
    st.subheader("Complete CSV QA Chat History")
    for role, msg in st.session_state.csv_chat:
        st.write(f"**{role}:**")
        st.write(msg)
        st.write("---")


elif agent_option == "Sunbeam Web Scraper":
    st.title("Sunbeam Internship Web Scraper")

   
    def scrape_sunbeam_raw():
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)
        driver.implicitly_wait(5)

        try:
            driver.get("https://www.sunbeaminfo.in/internship")
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            try:
                plus_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
                time.sleep(1)
                plus_button.click()
                time.sleep(2)
            except Exception:
                pass

            para_elements = driver.find_elements(By.CSS_SELECTOR, ".main_info.wow.fadeInUp")
            internship_info = "\n".join(p.text for p in para_elements if p.text)

            table_rows = driver.find_elements(By.TAG_NAME, "tr")
            batches = []
            for row in table_rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) < 8:
                    continue
                batches.append({
                    "Sr": cols[0].text,
                    "Batch": cols[1].text,
                    "Duration": cols[2].text,
                    "Start Date": cols[3].text,
                    "End Date": cols[4].text,
                    "Time": cols[5].text,
                    "Fees": cols[6].text,
                    "Download": cols[7].text
                })

            driver.quit()
            return {"internship_info": internship_info, "batches": batches}

        except Exception as e:
            driver.quit()
            return {"internship_info": f"Error: {e}", "batches": []}

    @tool
    def scrape_sunbeam(_: str):
        """
        Scrapes Sunbeam internship and batch information.
        Returns a dictionary with internship info and batch details.
        """
        return scrape_sunbeam_raw()

    web_agent = create_agent(
        model=llm,
        tools=[scrape_sunbeam],
        system_prompt=(
            "You are a web scraping agent.\n"
            "You MUST use the scrape_sunbeam tool.\n"
            "Answer ONLY Sunbeam internship or batch questions.\n"
            "Explain answers in very simple English."
        )
    )

    question = st.text_input("Ask about Sunbeam internship or batches")

    if st.button("Run Web Agent") and question:
        st.session_state.sunbeam_chat.append(("User", question))

        if "sunbeam" not in question.lower():
            answer = "* This agent only answers Sunbeam internship related questions."
            batches = []
            internship_info = ""
        else:
            response = web_agent.invoke({"messages": [{"role": "user", "content": question}]})
            answer = response["messages"][-1].content

            scraped_data = scrape_sunbeam_raw()
            internship_info = scraped_data["internship_info"]
            batches = scraped_data["batches"]

        st.session_state.sunbeam_chat.append(("Web Agent", answer))

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Internship Information")
        st.write(internship_info)

        if batches:
            st.subheader("Batch Details")
            st.dataframe(pd.DataFrame(batches))

  
    st.subheader("Complete Sunbeam Chat History")
    for role, msg in st.session_state.sunbeam_chat:
        st.write(f"**{role}:**")
        st.write(msg)
        st.write("---")
