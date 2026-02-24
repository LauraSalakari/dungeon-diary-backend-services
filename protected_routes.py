from api import retrieve_answer_phb, generate_notes_summary
from fastapi import Response, status, HTTPException, APIRouter, Depends
from pydantic import BaseModel
from mongodb import require_user, CampaignCreate, db_create_campaign, get_current_user_id, CampaignJoinSchema, \
    db_join_campaign, NoteSchema, create_new_note

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

    except HTTPException:
        # Let FastAPI handle it properly (401, 403, etc.)
        raise

    except Exception as e:
        # Real server error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/create-campaign")
def create_campaign(payload: CampaignCreate, user_id: str = Depends(get_current_user_id)):
    try:
        campaign, campaign_id = db_create_campaign(payload, user_id)

        return {
            "id": str(campaign_id),
            "name": campaign["name"],
            "join_code": campaign["join_code"],
        }

    except HTTPException:
        # Let FastAPI handle it properly (401, 403, etc.)
        raise

    except Exception as e:
        # Real server error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.post("/join-campaign")
def join_campaign(payload: CampaignJoinSchema, user_id: str = Depends(get_current_user_id)):
    try:
        campaign = db_join_campaign(payload, user_id)
        return {
            "campaign_id": str(campaign["campaign_id"]),
            "player_name": campaign["character_name"],
        }

    except HTTPException:
        # Let FastAPI handle it properly (401, 403, etc.)
        raise

    except Exception as e:
        # Real server error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.post("/add-note")
def add_note(payload: NoteSchema, user_id: str = Depends(get_current_user_id)):
    try:
        note = create_new_note(payload, user_id)

        return {
            "user_id": str(note["user_id"]),
            "campaign_id": str(note["campaign_id"]),
            "content": note["content"],
            "is_private": note["is_private"],
            "id": str(note["id"]),
            "session_date": note["session_date"]
        }

    except HTTPException:
        # Let FastAPI handle it properly (401, 403, etc.)
        raise

    except Exception as e:
        # Real server error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )