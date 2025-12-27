import os
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings

DATA_DIR ="resumes"
DB_PATH ="chroma_db"

os.makedirs(DATA_DIR,exist_ok=True)

embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = chromadb.Client(settings=chromadb.Settings(persist_directory=DB_PATH))
store = db.get_or_create_collection(name="resume_store")


def read_pdf(path):
    loader=PyPDFLoader(path)
    pages=loader.load()
    return "\n".join(p.page_content for p in pages)


def save_resume(name, text):
    rid=name.replace(".pdf","")
    vec =embedder.embed_documents([text])[0]
    store.add(
        ids=[rid],
        documents=[text],
        embeddings=[vec],
        metadatas=[{"file":name}]
    )


def upload_resume(file):
    path=os.path.join(DATA_DIR,file.name)
    with open(path,"wb") as f:
        f.write(file.getbuffer())
    text=read_pdf(path)
    save_resume(file.name,text)


def load_folder():
    for name in os.listdir(DATA_DIR):
        if name.endswith(".pdf"):
            rid=name.replace(".pdf", "")
            found=store.get(ids=[rid])
            if not found["ids"]:
                text=read_pdf(os.path.join(DATA_DIR, name))
                save_resume(name, text)


def find(query,top_k=3):
    qvec=embedder.embed_query(query)
    return store.query(query_embeddings=[qvec],n_results=top_k)


def remove(rid):
    store.delete(ids=[rid])


def resume_retriever(query, top_k=3):
    """Return combined text of top-K resumes for agent prompt."""
    results=find(query, top_k)
    if not results["ids"]:
        return "No resumes found"
    combined_text=""
    for i in range(len(results["ids"][0])):
        rid=results["ids"][0][i]
        text=results["documents"][0][i]
        combined_text+=f"Resume {i+1} ({rid}):\n{text}\n\n"
    return combined_text

