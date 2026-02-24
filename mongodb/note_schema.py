from datetime import datetime, timezone
from pydantic import BaseModel
from bson import ObjectId

from mongodb import notes_collection


class NoteSchema(BaseModel):
    campaign_id: str
    content: str
    is_private: bool
    session_date: str

class GetNotesRequest(BaseModel):
    campaign_id: str
    session_date: str


# probably can operate with just the note schema since it seems the summary will fit the same shape
class SummarySchema(BaseModel):
    userId: str
    campaignId: str
    content: str
    isPrivate: bool
    sessionDate: datetime

def set_session_date(date: str):
    """
    Generate a proper and standardised timestamp for the session date from the string coming from frontend
    :param date: date in string format YYYY-MM-DD
    :return: datetime object
    """
    std_date = datetime.strptime(date, '%Y-%m-%d')
    return std_date.replace(tzinfo=timezone.utc)


def create_new_note(note: NoteSchema, user_id: str):
    note_doc = {
        "user_id": user_id,
        "campaign_id": ObjectId(note.campaign_id),
        "content": note.content,
        "is_private": note.is_private,
        "session_date": set_session_date(note.session_date)
    }

    note = notes_collection.insert_one(note_doc)

    return {
        **note_doc,
        "id": note.inserted_id
    }

def get_personal_notes_from_db(info: GetNotesRequest, user_id: str):
    session = set_session_date(info.session_date)
    campaign = ObjectId(info.campaign_id)

    notes = notes_collection.find({"user_id": str(user_id), "campaign_id": campaign, "session_date": session})

    notes_clean = []

    for n in list(notes):
        clean_note = {
            "content": n["content"],
            "is_private": n["is_private"],
            "session_date": n["session_date"]
        }

        notes_clean.append(clean_note)

    print(notes_clean)

    return notes_clean