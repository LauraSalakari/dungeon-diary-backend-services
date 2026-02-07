from .utils import create_embeddings
from db import get_vectordb
from .ministral_utils import get_rag_answer

collection_name = "PHB2024"

# create PHB vectorDB
def create_phb_embeddings():
    """
    Generates the chromaDB for the Player's Handbook
    :return: None
    """
    create_embeddings("assets/PHB2024.pdf", collection_name)


def format_context(docs: list):
    prompt = "\n"
    for doc in docs:
        prompt += "\nContent:\n"
        prompt += doc.page_content + "\n\n"
    return prompt

# chatbot/LLM functionality
def retrieve_answer_phb(q: str, k: int = 5):
    """
    Retrieve relevant info about a question from the Player's Handbook
    :param q: User question
    :param k: Number of context options to retrieve
    :return: List of relevant documents from the vector database
    """

    db = get_vectordb(collection_name)
    context = db.similarity_search(q, k)
    formatted_context = format_context(context)

    return get_rag_answer(q, formatted_context)