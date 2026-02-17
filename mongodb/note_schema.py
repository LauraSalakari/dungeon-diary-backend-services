from datetime import datetime
from pydantic import BaseModel

class NoteSchema(BaseModel):
    userId: str
    campaignId: str
    content: str
    isPrivate: bool
    sessionDate: datetime       # TODO decide on this format


# probably can operate with just the note schema since it seems the summary will fit the same shape
class SummarySchema(BaseModel):
    userId: str
    campaignId: str
    content: str
    isPrivate: bool
    sessionDate: datetime