from pathlib import Path
import re
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(text: str) -> str:
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # remove browser/pdf footer noise
        if "FDIC.gov" in line:
            continue
        if "https://" in line or "http://" in line:
            continue
        if re.search(r"\d{1,2}/\d{1,2}/\d{2}", line):
            continue
        if re.search(r"\b\d+/\d+\b", line):
            continue

        cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines)

    # fix common ligatures
    cleaned_text = cleaned_text.replace("ﬀ", "ff")
    cleaned_text = cleaned_text.replace("ﬁ", "fi")
    cleaned_text = cleaned_text.replace("ﬂ", "fl")
    cleaned_text = cleaned_text.replace("ﬃ", "ffi")
    cleaned_text = cleaned_text.replace("ﬄ", "ffl")

    # normalize spaces/newlines
    cleaned_text = re.sub(r"[ \t]+", " ", cleaned_text)
    cleaned_text = re.sub(r"\n{2,}", "\n", cleaned_text)

    return cleaned_text.strip()


def load_all_pdfs(folder_path: str):
    all_docs = []
    pdf_files = Path(folder_path).glob("*.pdf")

    for pdf_file in pdf_files:
        loader = PyPDFLoader(
            str(pdf_file),
            mode="single"
        )
        docs = loader.load()

        for doc in docs:
            doc.metadata["source_file"] = pdf_file.name
            doc.page_content = clean_text(doc.page_content)

        all_docs.extend(docs)

    return all_docs


def is_good_chunk(text: str) -> bool:
    text = text.strip()

    if len(text) < 200:
        return False

    if "FDIC.gov" in text:
        return False
    if "http://" in text or "https://" in text:
        return False

    return True


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300,
        add_start_index=True
    )

    split_docs = splitter.split_documents(documents)
    split_docs = [doc for doc in split_docs if is_good_chunk(doc.page_content)]
    return split_docs


if __name__ == "__main__":
    folder = "data/raw_docs"

    docs = load_all_pdfs(folder)
    print(f"Loaded {len(docs)} PDF documents")
    print()

    split_docs = split_documents(docs)
    print(f"Created {len(split_docs)} chunks")
    print()

    for i, doc in enumerate(split_docs[:5]):
        print("=" * 80)
        print("CHUNK:", i)
        print("SOURCE:", doc.metadata.get("source_file"))
        print("START INDEX:", doc.metadata.get("start_index"))
        print(doc.page_content)
        print()