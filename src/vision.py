import ollama
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_PATH = "../vector_db/audi_chroma_db"
EMBEDDING_MODEL = "mxbai-embed-large"

def get_multimodal_answer(user_text=None, image_path=None):
    
  # 1. Image Processing (if image exists)
  identified_part = ""
  if image_path:
    print("--- 📸 Processing Image ---")
    vision_res = ollama.chat(
      model='llama3.2-vision',
      messages=[{
        'role': 'user',
        'content': 'Identify this Audi car part. Output only the technical name.',
        'images': [image_path]
      }]
    )
    identified_part = vision_res['message']['content']
