# Banking GenAI Assistant

A Streamlit + FastAPI based Retrieval-Augmented Generation (RAG) application that answers banking compliance questions using indexed FDIC compliance documents.

## Features

- Ask grounded compliance-related questions
- Retrieve relevant chunks from FDIC documents
- Generate answers based only on retrieved sources
- Show source chunks used for the answer
- Display query summary and grounding note
- Maintain recent chat history in the Streamlit app

## Project Structure

```text
banking-genai-assistant/
│
├── backend/
│   ├── __init__.py
│   └── main.py
│
├── src/
│   ├── __init__.py
│   └── rag_answer.py
│
├── data/
├── chroma_db/
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

Tech Stack
Streamlit
FastAPI
LangChain
ChromaDB
OpenAI Embeddings
Python
Setup Instructions
1. Open the project folder
cd C:\Users\vanda\Desktop\_\Sample_Project\banking-genai-assistant
2. Create virtual environment
python -m venv venv
3. Activate virtual environment
.\venv\Scripts\Activate
4. Install dependencies
pip install -r requirements.txt
Environment Variables

Create a .env file in the project root.

Example:

OPENAI_API_KEY=your_openai_api_key_here
BACKEND_URL=http://127.0.0.1:8000
How to Run the Project
Run the backend

From the project root:

uvicorn backend.main:app --reload

Backend runs at:

http://127.0.0.1:8000

FastAPI docs:

http://127.0.0.1:8000/docs
Run the frontend

Open a second terminal, activate the same virtual environment, then run:

streamlit run app.py

Frontend runs at:

http://localhost:8501
How the App Works
User enters a banking compliance question in the Streamlit UI
Streamlit sends the question to the FastAPI backend
Backend retrieves relevant document chunks from the vector database
The RAG pipeline generates an answer grounded in the retrieved chunks
The frontend displays:
generated answer
retrieved sources
query summary
recent chat history
Example Questions
What is a compliance management system?
What are the main components of an effective CMS?
Who is responsible for developing and administering a CMS?
What is the purpose of the Consumer Compliance Examination Manual?
Why is documentation important during an examination?
Notes
The app is designed to answer questions only from indexed FDIC compliance documents
Answers are grounded in retrieved document chunks
Local development uses FastAPI on port 8000 and Streamlit on port 8501
Troubleshooting
Backend connection error

If Streamlit cannot connect to the backend:

make sure FastAPI is running
verify backend is available at http://127.0.0.1:8000
check BACKEND_URL in .env
Module import error

If you get errors like ModuleNotFoundError, run the backend from the project root:
uvicorn backend.main:app --reload
No answer returned

Check:

backend logs
vector database exists
required documents are indexed
OpenAI API key is set correctly
Future Improvements
Better conversation memory
Follow-up question handling
Cleaner source cards
Upload and index new PDFs
Deployment to cloud
Authentication and user access control
License

This project is for educational and demo purposes.