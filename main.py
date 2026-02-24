from fastapi import FastAPI, status, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from mongodb import authenticate_user, create_access_token, UserCreate, hash_password, user_collection, \
    UserCreatedResult, UserLogin
from pymongo.errors import DuplicateKeyError
import protected_routes as protected

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


# add the protected router to the app
app.include_router(protected.router)