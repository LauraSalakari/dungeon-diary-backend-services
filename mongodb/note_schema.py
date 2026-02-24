from datetime import datetime, timezone
from pydantic import BaseModel
from bson import ObjectId

from mongodb import notes_collection


class NoteSchema(BaseModel):
    campaign_id: str
    content: str
    is_private: bool
    session_date: str       # TODO decide on this format


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