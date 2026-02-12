from api import retrieve_answer_phb, generate_notes_summary
from fastapi import FastAPI, Response, status, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()
web_url = os.getenv("WEB_URL")

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[web_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# dummy websocket
@app.websocket("/")
async def ignore_ws(ws: WebSocket):
    await ws.accept()
    await ws.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# for FastAPI to recognise what should be the request body, need to define it through pydantic
class PhbQuery(BaseModel):
    q: str

@app.post("/phb-rag")
def query_phb_rag (query: PhbQuery, res: Response):
    print("Question received:", query)
    try:
        answer = retrieve_answer_phb(query.q)
        res.status_code = status.HTTP_200_OK
        return answer
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

class NotesToSummarise(BaseModel):
    notes: list[str]

@app.post("/notes-summarise")
def summarise_notes(query: NotesToSummarise, res: Response):
    try:
        summary = generate_notes_summary(query.notes)
        res.status_code = status.HTTP_200_OK
        return summary
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)