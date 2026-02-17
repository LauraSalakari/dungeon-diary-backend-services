from api import retrieve_answer_phb, generate_notes_summary
from fastapi import FastAPI, Response, status, HTTPException, WebSocket, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from mongodb import authenticate_user, create_access_token, require_user, UserCreate, hash_password, user_collection, \
    UserCreatedResult, UserLogin
from pymongo.errors import DuplicateKeyError

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

@app.post("/login")
def login(payload: UserLogin):
    user = authenticate_user(payload.email, payload.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(str(user["_id"]))
    return {"access_token": token, "token_type": "bearer"}


@app.post("/register",
          response_model=UserCreatedResult,
          status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate):
    user_doc = {
        "email": payload.email.lower(),
        "username": payload.username,
        "password_hash": hash_password(payload.password),
        "campaigns": []
    }

    try:
        result = user_collection.insert_one(user_doc)

    except DuplicateKeyError:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    return {
        "id": str(result.inserted_id),
        "username": user_doc["username"],
        "email": user_doc["email"],
    }


# use API router to protect routes that require an identified user
router = APIRouter(
    prefix="/api",
    dependencies=[Depends(require_user)]
)


# for FastAPI to recognise what should be the request body, need to define it through pydantic
class PhbQuery(BaseModel):
    q: str

@router.post("/phb-rag")
def query_phb_rag (query: PhbQuery, res: Response):
    print("Question received:", query)
    try:
        answer = retrieve_answer_phb(query.q)
        res.status_code = status.HTTP_200_OK
        return answer

    except HTTPException:
        # Let FastAPI handle it properly (401, 403, etc.)
        raise

    except Exception as e:
        # Real server error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


class NotesToSummarise(BaseModel):
    notes: list[str]

@router.post("/notes-summarise")
def summarise_notes(query: NotesToSummarise, res: Response):
    try:
        summary = generate_notes_summary(query.notes)
        res.status_code = status.HTTP_200_OK
        return summary
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


# add the protected router to the app
app.include_router(router)