from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from db import create_vectordb

# embedding
def create_embeddings(src: str, title: str):
    """
    Create embedding matrix for source.
    :param src: file path to text source to be embedded
    :param title: name for source to use for db creation
    :return: Chroma vector store
    """

    # load the document
    loader = PyPDFLoader(src)
    pages = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(pages)

    # create embeddings with loaded model and store into vectorDB
    db = create_vectordb(chunks, title)

    return db