import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def process_pdf(filePath):
  loader = PyPDFLoader(filePath)
  pages = loader.load_and_split()

  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=1000,
      chunk_overlap = 100,
      length_function=len,
      add_start_index=True,
  )

  chunks = text_splitter.split_documents(pages)
  for chunk in chunks:
    # To remove audi specific text from headers or footers
    chunk.page_content = chunk.page_content.replace("Audi A4 Service Manual", "")

  print(f"Created {len(chunks)} technical knowledge snippets.")
  return chunks

embeddings = HuggingFaceEmbeddings(model_name="mxbai-embed-large")

def create_vector_db(chunks):
  vector_db = Chroma.from_documents(
      documents=chunks,
      embedding=embeddings,
      persist_directory="../vector_db/audi_chroma_db"
  )
  print("Vector database created and persisted.")
  return vector_db
