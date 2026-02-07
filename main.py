from api import create_phb_embeddings
from api import retrieve_answer_phb
from fastapi import FastAPI

# create_phb_embeddings()

# a = retrieve_answer_phb("What are the wizard subclasses?")
# print(a)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}