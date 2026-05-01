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

  # 2. Combine for Search Query
  if identified_part and user_text:
    search_query = f"{identified_part}: {user_text}"
  else:
    search_query = user_text if user_text else identified_part

  # 3. RAG Search
  print(f"--- 🔍 Searching Manual for your query ---")
  embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
  db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    
  docs = db.similarity_search(search_query, k=3)
  context = "\n\n".join([d.page_content for d in docs])

  # final Reasoning
  print("--- 🤖 Generating Technical Answer ---")
  prompt = f"""
    You are an Audi Maintenance Expert. 
    User Question/Part: {search_query}
    
    Relevant Technical Manual Snippets:
    {context}
    
    Instruction: Answer the user's request using the manual snippets. 
    Mention torque specs and page numbers if they appear. 
    If the context doesn't contain the answer, say you can't find it in this manual.
    Do not hallucinate any information!
    """
    
  final_res = ollama.generate(model='mistral', prompt=prompt)
    
  return {
        "answer": final_res['response'],
        "identified_part": identified_part,
        "sources": docs
  }
