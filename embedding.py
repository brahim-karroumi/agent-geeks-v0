import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

from data import GUIDE

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("API_KEY"),
    timeout=60,
    max_retries=0,
)

EMBEDDING_MODEL = "openai/text-embedding-3-small"
PROJECT_DIR = Path(__file__).resolve().parent
CHROMA_PATH = Path(
    os.getenv("CHROMA_PATH", str(PROJECT_DIR / "chroma_db"))
)
COLLECTION_NAME = "morocco_guide"


def embed(texts):
    if isinstance(texts, str):
        inputs = [texts]
        single = True
    elif isinstance(texts, list) and texts and all(isinstance(t, str) for t in texts):
        inputs = texts
        single = False
    else:
        raise ValueError("texts must be a non-empty string or a list of strings.")

    if any(not t.strip() for t in inputs):
        raise ValueError("texts must not contain empty strings.")

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=inputs,
        encoding_format="float",
    )

    vectors = [item.embedding for item in sorted(response.data, key=lambda x: x.index)]
    return vectors[0] if single else vectors


def get_chroma_client():
    CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_PATH))


def get_collection():
    db = get_chroma_client()
    return db.get_or_create_collection(name=COLLECTION_NAME)


def build_local_db():
    chunks = [p.strip() for p in GUIDE.split("\n\n") if p.strip()]
    vectors = embed(chunks)
    collection = get_collection()

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=vectors,
    )

    return {
        "path": str(CHROMA_PATH),
        "collection": COLLECTION_NAME,
        "chunks": len(chunks),
    }


def search(query, n_results=3):
    collection = get_collection()
    query_vector = embed(query)
    return collection.query(
        query_embeddings=[query_vector],
        n_results=n_results,
    )


if __name__ == "__main__":
    result = build_local_db()
    print("Local Chroma DB created!")
    print(result)

    hits = search("How much is Majorelle?", n_results=2)
    print("Search test:", hits["documents"])
