# audi-ai-maintenance-copilot
# Multimodal AI Maintenance Copilot for Automotive Systems
**Specialized RAG System for Audi Technical Documentation**

## Overview
This project is an MVP developed as a passion project of mine and to help a customer of Audi (a friend). It leverages **Generative AI** and **Computer Vision** to provide instant maintenance guidance. Users can either type a query or upload a photo of a car component to receive precise instructions extracted from any official technical manual you choose to vectorize.

### Key Features
- **Local Multimodal RAG:** Uses Llama 3.2 Vision (via Ollama) for zero-cost image analysis.
- **Context-Aware Retrieval:** LangChain-based pipeline for searching Audi service manuals.
- **Privacy-First:** 100% local execution—no data leaves the machine (important for corporate data security).

## Tech Stack
- **Vision/LLM:** Llama 3.2-Vision & Llama 3.1 (Ollama)
- **Framework:** LangChain
- **Vector Store:** ChromaDB
- **UI:** Streamlit
- **Language:** Python 3.10+
- **To be implemented:** RAGAS, Langfuse, Guardrails, Docker to create a packaged file for ease of sharing and deployment.

## How to use it
- Fork the repository
- Run python -m venv .venv
- Add a service manual (as not included on the repository for privacy purposes) in data/raw/ and set name to that in ingestion.py
- Download the ollama models on your system
- Run ingestion.py
- Run app.py

## Disclaimer
- It is heavily focused on local and privacy oriented use. Hence why steps must be taken to run the app locally.