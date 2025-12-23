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
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

st.title("Multi-Agent System")

if "chat" not in st.session_state:
    st.session_state.chat = []

llm = init_chat_model(
    model="phi-3-mini-4k-instruct",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy_key",
    temperature=0
)

st.header("1️⃣ CSV  Agent")
file = st.file_uploader("Upload CSV file", type="csv")

if file:
    df = pd.read_csv(file)

    st.subheader("CSV Schema")
    st.write(df.dtypes)

    @tool
    def run_csv_sql(query: str) -> str:
        """Execute SQL on uploaded CSV and return results"""
        try:
            result = sqldf(query, {"data": df})
            return result.to_string(index=False)
        except Exception as e:
            return f"SQL Error: {e}"

    csv_question = st.text_input("Ask a question about the CSV data")

    if st.button("Run CSV Agent") and csv_question:
        st.session_state.chat.append(("User", csv_question))

        
        sql_prompt = f"""
Convert the following question into SQL.
Table name is 'data'.

Schema:
{df.dtypes}

Question:
{csv_question}

Return only SQL.
"""
        sql = llm.invoke(sql_prompt).content.strip()
        sql = sql.replace("```sql", "").replace("```", "").strip()

        
        explain_prompt = f"""
Explain this SQL query in very simple English.

SQL:
{sql}
"""
        explanation = llm.invoke(explain_prompt).content.strip()        
        result = run_csv_sql.run(sql)
        response = f"""
SQL:
{sql}

Explanation:
{explanation}

Result:
{result}
"""
        st.session_state.chat.append(("CSV Agent", response))

        st.code(sql, "sql")
        st.write("Explanation:")
        st.write(explanation)
        st.write("Result:")
        st.text(result)


st.header("2️⃣ Web Scraping Agent")

@tool
def scrape_sunbeam_internship(tool_input: str) -> dict:
    """Scrape Sunbeam internship and batch info directly from Sunbeam website"""
    driver = webdriver.Chrome()  # simple style
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
        internship_info = "\n".join([p.text for p in para_elements])
       
        table_rows = driver.find_elements(By.TAG_NAME, "tr")
        batches = []
        for row in table_rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 8:
                continue
            info = {
                "Sr": cols[0].text,
                "Batch": cols[1].text,
                "Duration": cols[2].text,
                "Start Date": cols[3].text,
                "End Date": cols[4].text,
                "Time": cols[5].text,
                "Fees": cols[6].text,
                "Download": cols[7].text
            }
            batches.append(info)

        driver.quit()
        return {"internship_info": internship_info, "batches": batches}

    except Exception as e:
        driver.quit()
        return {"internship_info": f"Error: {e}", "batches": []}

sunbeam_question = st.text_input("Ask about Sunbeam internship or batch information")

if st.button("Run ") and sunbeam_question:
    st.session_state.chat.append(("User", sunbeam_question))
    
    scraped_data = scrape_sunbeam_internship.run("")

    internship_info = scraped_data["internship_info"]
    batches = scraped_data["batches"]

    web_prompt = f"""
The following text is scraped from the Sunbeam website.

Website Content:
{internship_info}

User Question:
{sunbeam_question}

Answer the question clearly and explain in very simple English.
"""
    answer = llm.invoke(web_prompt).content.strip()
    st.session_state.chat.append(("Web Agent", answer))

    st.write("Answer:")
    st.write(answer)

    st.subheader("Internship Info:")
    st.write(internship_info)

    st.subheader("Internship Batches:")
    if batches:
        st.dataframe(pd.DataFrame(batches))
    else:
        st.write("No batch data found.")


st.header("Complete Chat History")
for role, msg in st.session_state.chat:
    st.write(f"**{role}:**")
    st.write(msg)
    st.write("---")
