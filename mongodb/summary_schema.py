from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel
from api import generate_notes_summary
from mongodb import notes_collection, summary_collection
from mongodb.note_schema import set_session_date


class SummarySchema(BaseModel):
    campaign_id: str
    user_id: str
    contains_public: bool
    summary_content: str
    session_date: datetime

class SummaryCreateSchema(BaseModel):
    campaign_id: str
    contains_public: bool
    session_date: str

def query_private_notes(campaign, session, user_id):
    return {
        "campaign_id": campaign,
        "session_date": session,
        "user_id": user_id,
    }

def query_public_notes(campaign, session, user_id):
    return {
        "campaign_id": campaign,
        "session_date": session,
        "$or": [
            {"userId": user_id},
            {
                "$and": [
                    {"user_id": {"$ne": user_id}},
                    {"is_private": False}
                ]
            }
        ]
    }

def generate_summary(req: SummaryCreateSchema, user_id: str):
    campaign = ObjectId(req.campaign_id)
    session = set_session_date(req.session_date)

    query = query_public_notes(campaign, session, user_id) if req.contains_public else query_private_notes(campaign, session, user_id)

    notes = list(notes_collection.find(query).sort("created_at", 1))

    notes_for_llm = []
    for note in notes:
        notes_for_llm.append(note["content"])

    print(notes_for_llm)

    summary = generate_notes_summary(notes_for_llm)

    summary_collection.insert_one({
        "campaign_id": campaign,
        "user_id": user_id,
        "contains_public": req.contains_public,
        "summary_content": summary,
        "session_date": session,
    })

    return {
        "contains_public": req.contains_public,
        "summary_content": summary,
        "session_date": session,
    }

def fetch_summaries(campaign_id: str, session_date: str, user_id: str):
    session = set_session_date(session_date)

    summaries = list(summary_collection.find({
        "campaign_id": ObjectId(campaign_id),
        "session_date": session,
        "user_id": user_id,
    }))

    print(summaries)
    return summaries
