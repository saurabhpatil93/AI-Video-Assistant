
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


# =========================
# Configuration
# =========================

CHROMA_DIR = "vector_db"
COLLECTION_NAME = "meeting_transcript"
EMBEDDING_MODEL = "nomic-embed-text"


# =========================
# Get Ollama Embeddings
# =========================

def get_embeddings():

    return OllamaEmbeddings(
        model=EMBEDDING_MODEL
    )


# =========================
# Build Vector Store
# =========================

def build_vector_store(transcript: str) -> Chroma:

    print("Building vector store...")

    # Split transcript into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(transcript)

    print(f"Created {len(chunks)} chunks.")

    # Convert chunks into Documents
    docs = [
        Document(
            page_content=chunk,
            metadata={
                "chunk_index": i
            }
        )
        for i, chunk in enumerate(chunks)
    ]

    # Get Ollama embedding model
    embeddings = get_embeddings()

    # Create Chroma vector store
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR
    )

    print("Vector store created successfully.")

    return vector_store


# =========================
# Load Vector Store
# =========================

def load_vector_store() -> Chroma:

    print("Loading vector store...")

    embeddings = get_embeddings()

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR
    )

    print("Vector store loaded successfully.")

    return vector_store


# =========================
# Get Retriever
# =========================

def get_retriever(
    vector_store: Chroma,
    k: int = 4
):

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k
        }
    )
