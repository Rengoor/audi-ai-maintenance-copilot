from langchain_ollama import OllamaEmbeddings

# Shared Settings
DB_PATH = "../vector_db/audi_chroma_db"
EMBEDDING_MODEL_NAME = "mxbai-embed-large"
VISION_MODEL_NAME = "llama3.2-vision"
TEXT_MODEL_NAME = "mistral"


def get_embedding_model():
    return OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)


def get_db_path():
    return DB_PATH


def get_vision_model():
    return VISION_MODEL_NAME


def get_text_model():
    return TEXT_MODEL_NAME
