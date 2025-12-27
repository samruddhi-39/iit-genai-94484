import streamlit as st
from vectorstore import upload_resume, load_folder, find, remove, store
from agent import run_agent

st.title("Resume Shortlisting System")

if st.button("Load resumes"):
    load_folder()
    st.success("Resumes loaded")

file = st.file_uploader("Upload resume (PDF)", type=["pdf"])
if file:
    upload_resume(file)
    st.success("Resume saved")

query = st.text_area("Enter Job Description")
top_k = st.slider("Top results", 1, 10, 3)

if st.button("Search"):
    if query.strip():
        ans = run_agent(query)
        st.subheader("Agentic Resume Ranking")
        st.text(ans)
    else:
        st.error("Enter Job Description first")

st.header("Stored Resumes")
data = store.get()
if data["ids"]:
    for rid in data["ids"]:
        a, b = st.columns([4, 1])
        a.write(rid)
        if b.button("Delete", key=f"rm_{rid}"):
            remove(rid)
            st.warning(f"Deleted {rid}")
else:
    st.info("No resumes found")
