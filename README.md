# audi-ai-maintenance-copilot
# Multimodal AI Maintenance Copilot for Automotive Systems
**Specialized RAG System for Audi Technical Documentation**

## 🚗 Overview
This project is an MVP developed for my 4th-semester project at **TH Ingolstadt**. It leverages **Generative AI** and **Computer Vision** to provide instant maintenance guidance. Users can either type a query or upload a photo of a car component to receive precise instructions extracted from official technical manuals.

### Key Features
- **Local Multimodal RAG:** Uses Llama 3.2 Vision (via Ollama) for zero-cost image analysis.
- **Context-Aware Retrieval:** LangChain-based pipeline for searching Audi service manuals.
- **Privacy-First:** 100% local execution—no data leaves the machine (important for corporate data security).

## 🛠 Tech Stack
- **Vision/LLM:** Llama 3.2-Vision & Llama 3.1 (Ollama)
- **Framework:** LangChain
- **Vector Store:** ChromaDB
- **UI:** Streamlit
- **Language:** Python 3.10+