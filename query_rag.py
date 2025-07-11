import os

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from config import VECTORSTORE_DIR, OPENAI_API_KEY

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def run_query(question):
  vectorstore = FAISS.load_local(
      VECTORSTORE_DIR,
      HuggingFaceEmbeddings(model_name="all-mpnet-base-v2"),
      allow_dangerous_deserialization=True
  )
  retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
  llm = ChatOpenAI(
      model="gpt-3.5-turbo",
      temperature=0.7,
      max_tokens=512
  )
  chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
  return chain.invoke(question)

if __name__ == "__main__":
  while True:
    query = input("Ask Jobs-AI a question: ")
    answer = run_query(query)["result"]
    print(f"\n🧠 Jobs-AI says:\n{answer}\n")