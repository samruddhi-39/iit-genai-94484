from langchain_text_splitters import CharacterTextSplitter

raw_text = """This is some sample text that I want to split into chunks.
You can put your full document text here."""

text_splitter=CharacterTextSplitter(chunk_size=500,chunk_overlap=50)
docs=text_splitter.create_documents([raw_text])

for i, doc in enumerate(docs):
    print(f"--- Document {i+1} ---")
    print(doc)