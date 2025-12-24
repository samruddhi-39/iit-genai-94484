from langchain_text_splitters import RecursiveCharacterTextSplitter


raw_text = """
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

# More Python code...
"""


code_splitter = RecursiveCharacterTextSplitter.from_language(
    language="python", 
    chunk_size=100, 
    chunk_overlap=50 
)


docs = code_splitter.create_documents([raw_text])


for i, doc in enumerate(docs):
    print(f"--- Chunk {i+1} ---")
    print(doc)
