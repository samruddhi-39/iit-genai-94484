from langchain_text_splitters import TokenTextSplitter
raw_text = """This is some sample text that I want to split into chunks.
You can put your full document text here."""
text_splitter=TokenTextSplitter(chunk_size=10,chunk_overlap=5)
docs=text_splitter.create_documents([raw_text])

for i, doc in enumerate(docs):
    print(f"--- Chunk {i+1} ---")
    print(doc)