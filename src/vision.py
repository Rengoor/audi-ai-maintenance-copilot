import ollama
import re
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
            model="llama3.2-vision",
            messages=[
                {
                    "role": "user",
                    "content": "Identify this Audi car part. Output only the technical name.",
                    "images": [image_path],
                }
            ],
        )
        identified_part = vision_res["message"]["content"]

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
  
  Manual Snippets: {context}
    
  Instructions:
  - Use ONLY the provided snippets.
  - If you mention torque (Nm) or measurements, you MUST include the page number.
  - If the info is missing, state: "Specific technical data not found in provided manual snippets."
  - DO NOT HALLUCINATE!
  """
    final_res = ollama.generate(model="mistral", prompt=prompt)
    answer = final_res["response"]

    # SAFETY LOGIC
    # Scan for technical values that require double-checking
    safety_keywords = ["Nm", "torque", "tightening", "bar", "psi", "clearance", "bolt"]
    contains_measurements = any(
        word.lower() in answer.lower() for word in safety_keywords
    )

    safety_disclaimer = ""
    if contains_measurements:
        safety_disclaimer = (
            "\n\n⚠️ **SAFETY CHECK REQUIRED:** This response contains torque specifications or measurements. "
            "Please cross-reference with the source page numbers cited above before performing work."
        )

    # Extract unique page numbers for the UI to display cleanly
    source_pages = list(set([doc.metadata.get("page", "N/A") for doc in docs]))

    return {
        "answer": answer + safety_disclaimer,
        "identified_part": identified_part,
        "sources": docs,
        "requires_safety_check": contains_measurements,  # Useful for UI styling (e.g., red border)
    }
