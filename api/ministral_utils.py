from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
ministral_url = os.getenv("MINISTRAL_URL")

MODEL_ID = "mistralai/Ministral-3-3B-Instruct-2512"

client = OpenAI(
    base_url=ministral_url,
    api_key="not-needed"
)


def get_rag_answer(query: str, context):
    prompt = f"Answer the following question based on the context below:\n\n{context}\n\nQuestion: {query}\nAnswer:"

    resp = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You are a helpful assistant providing answers based on provided context."},
            {"role": "user", "content": prompt}
        ]
    )

    return resp.choices[0].message.content