from langchain_text_splitters import SentenceTransformersTokenTextSplitter

raw_text = """This is some sample text that I want to split into chunks.
You can put your full document text here."""
text_splitter = SentenceTransformersTokenTextSplitter(chunk_size=256, chunk_overlap=20)
docs = text_splitter.create_documents([raw_text])

for d in docs:
    print(d.page_content)