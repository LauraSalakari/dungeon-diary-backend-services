from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
ministral_url = os.getenv("MINISTRAL_URL")

MODEL_ID = "mistralai/Ministral-3-3B-Instruct-2512"

client = OpenAI(
    base_url=ministral_url,
    api_key="not-needed"        # currently the Ministral service expects no auth
)

# Ministral-3 is running locally in a Docker container available at the URL specified in the .env file

def get_rag_answer(query: str, context):
    """
    Uses the Ministral end-point to generate an answer based on the provided conxt
    :param query: User question
    :param context: Relevant context fetched from vector store
    :return: Generated answer in string format
    """
    prompt = f"Answer the following question based on the context below:\n\n{context}\n\nQuestion: {query}\nAnswer:"

    resp = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You are a helpful assistant providing answers based only on the provided context."},
            {"role": "user", "content": prompt}
        ]
    )

    return resp.choices[0].message.content


def generate_notes_summary(notes: list[str]):
    prompt = f"Summarise and combine the following notes, each separated by --: {' -- '.join(notes)}"

    resp = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You are helpful assistant creating simple summaries without injecting further information."},
            {"role": "user", "content": prompt},
        ]
    )

    return resp.choices[0].message.content