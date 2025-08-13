import os

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from config import (
  VECTORSTORE_DIR,
  OPENAI_API_KEY,
  EMBEDDING_MODEL,
  CHAT_MODEL,
  TEMPERATURE,
  MAX_TOKENS,
  TOP_K,
  OFFLINE_MODE,
)

os.environ["TOKENIZERS_PARALLELISM"] = "false"
if OPENAI_API_KEY:
  os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


PERSONA_TEMPLATE = """
You are Steve Jobs as an AI business coach. Speak with his trademark bluntness, intensity, and high standards.
- Be concise, brutally honest, and use occasional expletives for emphasis (never slurs; no targeted personal abuse).
- Ground your advice in Apple history, product vision, craftsmanship, and user obsession. Reference real stories when helpful.
- Always produce actionable guidance.

Context from retrieved documents:
{context}

User question:
{question}

Answer as Steve Jobs:
"""


def build_qa_chain(top_k: int | None = None):
  vectorstore = FAISS.load_local(
      VECTORSTORE_DIR,
      HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL),
      allow_dangerous_deserialization=True
  )
  retriever = vectorstore.as_retriever(search_kwargs={"k": (top_k or TOP_K)})
  llm = ChatOpenAI(
      model=CHAT_MODEL,
      temperature=TEMPERATURE,
      max_tokens=MAX_TOKENS,
  )
  prompt = PromptTemplate(
      input_variables=["context", "question"],
      template=PERSONA_TEMPLATE.strip(),
  )
  chain = RetrievalQA.from_chain_type(
      llm=llm,
      retriever=retriever,
      chain_type_kwargs={"prompt": prompt},
      return_source_documents=True,
  )
  return chain


def extract_sources(source_documents):
  sources = []
  for doc in source_documents or []:
    meta = doc.metadata or {}
    source = meta.get("source") or meta.get("file_path") or "unknown"
    page = meta.get("page")
    if page is not None:
      sources.append(f"{source}#page={page}")
    else:
      sources.append(str(source))
  return sources


def apply_guardrails(text: str) -> str:
  if not text:
    return text
  import re
  blocked_words = [
    "nigger", "nig", "retard", "spaz", "fag", "faggot", "chink", "spic",
  ]
  pattern = re.compile(r"\b(" + "|".join(map(re.escape, blocked_words)) + r")\b", flags=re.IGNORECASE)
  return pattern.sub("[redacted]", text)


def run_query(question: str, memory: str | None = None, top_k: int | None = None, include_sources: bool = False):
  if OFFLINE_MODE or not os.environ.get("OPENAI_API_KEY"):
    mock = "Be honest: you over-scoped. Cut features, polish the core, and ship. Tomorrow, one killer outcome—no fluff."
    return {"answer": apply_guardrails(mock), "sources": [] if include_sources else None}
  chain = build_qa_chain(top_k=top_k)
  combined_question = question if not memory else (
    f"User background/context (JSON):\n{memory}\n\nQuestion:\n{question}"
  )
  result = chain.invoke({"query": combined_question})
  answer = result.get("result") if isinstance(result, dict) else str(result)
  answer = apply_guardrails(answer)
  if include_sources:
    srcs = extract_sources(result.get("source_documents") if isinstance(result, dict) else None)
    return {"answer": answer, "sources": srcs}
  return {"answer": answer}


if __name__ == "__main__":
  while True:
    query = input("Ask Jobs-AI a question: ")
    result = run_query(query, include_sources=True)
    print(f"\n🧠 Jobs-AI says:\n{result['answer']}\n")
    if result.get("sources"):
      print("Sources:")
      for s in result["sources"]:
        print(f"- {s}")