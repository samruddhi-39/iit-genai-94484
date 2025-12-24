from langchain_text_splitters import RecursiveCharacterTextSplitter

raw_text = """This is some sample text that I want to split into chunks.
You can put your full document text here."""
text_splitter=RecursiveCharacterTextSplitter(chunk_size=800,chunk_overlap=100,
separators=["\n\n","\n"," ",""])
docs=text_splitter.create_documents([raw_text])

# Optional: check the result
for i, doc in enumerate(docs):
    print(f"--- Document {i+1} ---")
    print(doc)