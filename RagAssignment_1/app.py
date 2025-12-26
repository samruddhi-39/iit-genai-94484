import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document


RESUME_DIR = "resumes"
DB_DIR = "chroma_db"

os.makedirs(RESUME_DIR, exist_ok=True)

# Embeddings & LLM
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": False}
)

llm = ChatOpenAI(
    model="phi-3-mini-4k-instruct",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed",
    temperature=0
)

vector_db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings
)


#  email/phone extraction 
def extract_email_phone(text):
    email, phone = "Not Found", "Not Found"

    
    if "@" in text:
        words = text.split()
        for w in words:
            if "@" in w and "." in w:
                email = w
                break

    
    digits = "".join(c if c.isdigit() else "" for c in text)
    if len(digits) >= 10:
        phone = digits[:10]

    return email, phone

# Add/update resume
def add_or_update_resume(pdf_path, resume_id):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    full_text = " ".join(p.page_content for p in pages)

    email, phone = extract_email_phone(full_text)

    vector_db._collection.delete(where={"resume_id": resume_id})
    doc = Document(
        page_content=full_text,
        metadata={
            "resume_id": resume_id,
            "email": email,
            "phone": phone
        }
    )
    vector_db.add_documents([doc])
    vector_db.persist()

# Delete resume
def delete_resume(resume_id):
    vector_db._collection.delete(where={"resume_id": resume_id})
    vector_db.persist()

# List stored resumes
def list_resumes():
    data = vector_db.get(include=["metadatas"])
    if not data["metadatas"]:
        return []
    return sorted(set(m["resume_id"] for m in data["metadatas"]))

# Shortlist resumes
def shortlist_resumes(job_description, top_k):
    return vector_db.similarity_search(job_description, k=top_k)

# Generate explanation
def generate_candidate_explanation(resume_text, job_description):
    prompt = f"""
You are an AI resume shortlisting assistant.

Using ONLY the resume content below, explain why this candidate
is suitable or not suitable for the given job description.
Do not use any external knowledge.

Resume:
{resume_text}

Job Description:
{job_description}
"""
    return llm.invoke(prompt).content

#  STREAMLIT UI --------
st.set_page_config(page_title="AI Resume Shortlisting")
st.title("AI Resume Shortlisting System")

# Add new resume
st.header("Add New Resume")
uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])
if uploaded_file:
    save_path = os.path.join(RESUME_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    add_or_update_resume(save_path, uploaded_file.name)
    st.success(f"Resume '{uploaded_file.name}' added successfully")

# Load all resumes from directory
st.header("Load / Update Resumes from Directory")
if st.button("Load All Resumes"):
    for file in os.listdir(RESUME_DIR):
        if file.endswith(".pdf"):
            add_or_update_resume(os.path.join(RESUME_DIR, file), file)
    st.success("All resumes loaded successfully")

# Stored resumes
st.header("Stored Resumes")
resume_ids = list_resumes()
if resume_ids:
    for r in resume_ids:
        st.write("•", r)
else:
    st.info("No resumes stored yet")

# Delete resume..
st.header("Delete Resume")
delete_id = st.selectbox("Select Resume", [""] + resume_ids)
if st.button("Delete Selected Resume") and delete_id:
    delete_resume(delete_id)
    st.success("Resume deleted successfully")

# Shortlisting
st.header("Resume Shortlisting & Ranking")
job_description = st.text_area("Enter Job Description")
top_k = st.number_input("Top-K Resumes", min_value=1, max_value=10, value=3)

if st.button("Shortlist & Rank"):
    if job_description.strip():
        results = shortlist_resumes(job_description, top_k)
        st.subheader("Ranked Shortlisted Candidates")
        for rank, doc in enumerate(results, 1):
            st.markdown(f"## Rank {rank}")
            st.write(f" Resume: {doc.metadata['resume_id']}")
            st.write(f" Email: {doc.metadata.get('email')}")
            st.write(f" Phone: {doc.metadata.get('phone')}")
            explanation = generate_candidate_explanation(doc.page_content, job_description)
            st.markdown("**Explanation:**")
            st.write(explanation)
            st.divider()
    else:
        st.warning("Please enter job description")
