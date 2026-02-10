from starlette.middleware.trustedhost import TrustedHostMiddleware

from api import create_phb_embeddings
from api import retrieve_answer_phb
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

# create_phb_embeddings()

# a = retrieve_answer_phb("What are the wizard subclasses?")
# print(a)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

class PhbQuery(BaseModel):
    q: str

@app.post("/phb-rag")
def query_phb_rag (query: PhbQuery, res: Response):
    print("Question received:", query)
    try:
        res.status_code = status.HTTP_200_OK
        return retrieve_answer_phb(query.q)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)