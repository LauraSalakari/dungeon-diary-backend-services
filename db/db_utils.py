import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

PERSIST_DIRECTORY = "db"

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    encode_kwargs={"normalize_embeddings": True}
)

client = chromadb.Client(
    chromadb.config.Settings(
        persist_directory=PERSIST_DIRECTORY,
        is_persistent=True
    )
)

def get_vectordb(collection_name: str) -> Chroma:
    """
    Load an existing vectordb collection.
    :param collection_name: VectorDB to load
    :return: Chroma vectorDB
    """
    return Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings
    )

def create_vectordb(docs, collection_name: str) -> Chroma:
    """
    Create a new vectordb collection.
    :param docs: documents to embed
    :param collection_name: VectorDB collection name
    :return: Chroma vectorDB
    """

    return Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=collection_name,
        client=client
    )