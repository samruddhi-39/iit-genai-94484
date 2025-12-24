
from langchain_text_splitters import MarkdownHeaderTextSplitter

markdown_text = """
# Introduction
This is the introduction section.

## Background
This section explains the background.

### Details
Here are some detailed points.

## Conclusion
This is the conclusion section.
"""
headers_to_split_on = [ ("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3") ]
text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
docs = text_splitter.split_text(markdown_text)
for i, doc in enumerate(docs):
    print(f"--- Chunk {i+1} ---")
    print(doc)