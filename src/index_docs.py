import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from src.langchain_loader import load_all_pdfs, split_documents

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def build_vector_store():
    docs = load_all_pdfs("data/raw_docs")
    split_docs = split_documents(docs)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=api_key
    )

    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory="chroma_db",
        collection_name="fdic_docs"
    )

    print(f"Indexed {len(split_docs)} chunks into Chroma.")
    return vectorstore


if __name__ == "__main__":
    build_vector_store()