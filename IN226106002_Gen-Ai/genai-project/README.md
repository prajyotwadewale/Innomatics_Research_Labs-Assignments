# 🚀 RAG-Based Customer Support Assistant with LangGraph and HITL

## 📌 Overview
This project implements a **Retrieval-Augmented Generation (RAG)** based Customer Support Assistant that answers user queries from a PDF knowledge base.

It uses:
- LangGraph for workflow orchestration  
- ChromaDB for vector storage  
- Groq LLM for response generation  
- Human-in-the-Loop (HITL) for escalation  

---

## 🎯 Key Features

- 📄 Upload PDF dynamically
- 🔍 Context-based retrieval using embeddings
- 🧠 LLM-based answer generation
- 🔗 LangGraph workflow orchestration
- ⚡ Conditional routing (Answer / HITL)
- 👨‍💻 Human-in-the-Loop escalation
- 💬 Streamlit UI
- 📊 Confidence scoring

---

## 📂 Project Structure
```text
genai-project/
│
├── app.py
├── main.py
├── graph.py
├── hitl.py
├── retriever.py
├── vector_store.py
├── embeddings.py
├── chunking.py
├── document_loader.py
│
├── data/
├── chroma_db/
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run

```bash
git clone https://github.com/prajyotwadewale/Innomatics_Research_Labs-Assignments.git
cd Innomatics_Research_Labs-Assignments/IN226106002_Gen-Ai/genai-project

python -m venv venv
venv\Scripts\activate   # (Windows)

pip install -r requirements.txt

# create .env file and add:
# GROQ_API_KEY=your_api_key_here

python -m streamlit run app.py
```

---

## 🌐 Open in Browser
Open: `http://localhost:8501`

---

## 💡 How to Use

1. Upload a PDF from the sidebar  
2. Wait for processing  
3. Ask questions  
4. View answer + confidence  
5. If query is not found → HITL escalation  

---

## 🧪 Example Queries

- What is this document about?  
- List all events  
- Explain key points  
- How many volunteers are there?  

---

## ⚠️ Important Notes

- Do NOT upload:
  - `venv/`
  - `.env`
  - `chroma_db/`
- Always keep API key secure

---

## 🔮 Future Enhancements

- Multi-document support  
- Chat memory  
- Source citations  
- Hybrid search  

---

## 👨‍💻 Author
**Prajyot Wadewale**

---

## ⭐ Acknowledgment
Built as part of a GenAI Internship Assignment focusing on RAG system design.
