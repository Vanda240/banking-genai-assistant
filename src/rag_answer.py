import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def generate_answer(query: str):
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

    context = "\n\n".join([doc.page_content for doc in results])

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=api_key,
        temperature=0
    )

    prompt = f"""
You are a banking compliance assistant.

Answer the user's question using only the provided context.
If the answer is not found in the context, say: "I could not find the answer in the provided documents."

Instructions:
- Give a direct answer in 2-3 sentences.
- Use clear, natural, professional wording.
- Paraphrase the source instead of copying awkward phrasing directly.
- Include the main components if the context provides them.
- Include important functions or responsibilities listed in the context when answering definitional questions.
- Do not omit key items if the source provides a list.
- Do not add information not supported by the context.



Context:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)

    sources = []
    for doc in results:
        sources.append({
            "source_file": doc.metadata.get("source_file"),
            "start_index": doc.metadata.get("start_index"),
            "content": doc.page_content
        })

    return response.content, sources


if __name__ == "__main__":
    while True:
        query = input("\nEnter your question (or type 'exit'): ").strip()

        if query.lower() == "exit":
            break

        answer, sources = generate_answer(query)
        print("\nANSWER:\n")
        print(answer)
        print("\nSOURCES:\n")
        for i, s in enumerate(sources, start=1):
            print(f"{i}. {s['source_file']} | start_index={s['start_index']}")
        print("\n" + "=" * 100 + "\n")