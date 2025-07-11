🧠 Steve Jobs RAG Chatbot
This project is a Retrieval-Augmented Generation (RAG) pipeline that lets you chat with a highly realistic AI version of Steve Jobs. The system retrieves real quotes, interviews, and transcripts from Jobs' life to ground each response in authentic material.

🛠️ Setup
Create a virtual environment and activate it:
python3 -m venv venv
source venv/bin/activate
Install dependencies
pip install -r requirements.txt
🚀 How to Run the Full Pipeline
1. Download all Steve Jobs source material from a Google Drive folder:

python3 download_files.py
2. Create and save the vector store:

python3 create_vectorstore.py
3. Ask Steve Jobs a question:

python3 query_rag.py# Jobs-rag
Steve Jobs RAG
