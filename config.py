from langchain_ollama import OllamaEmbeddings

# Shared Settings
DB_PATH = "./vector_db/audi_chroma_db"
EMBEDDING_MODEL_NAME = "mxbai-embed-large"


def get_embedding_model():
    return OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)


def get_db_path():
    return DB_PATH
