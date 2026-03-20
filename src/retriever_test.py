import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def test_retrieval(query: str):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=api_key
    )

    vectorstore = Chroma(
        collection_name="fdic_docs",
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    results = vectorstore.similarity_search(query, k=3)

    print(f"Query: {query}")
    print()

    for i, doc in enumerate(results, start=1):
        print("=" * 80)
        print("RESULT:", i)
        print("SOURCE:", doc.metadata.get("source_file"))
        print("START INDEX:", doc.metadata.get("start_index"))
        print(doc.page_content[:1200])
        print()


if __name__ == "__main__":
    test_retrieval("What is a compliance management system?")