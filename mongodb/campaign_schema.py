import secrets
import string
from typing import List
from pydantic import BaseModel
from . import user_collection
from .auth_utils import hash_password
from .get_database import campaign_collection
from bson import ObjectId

class PlayerCharacter(BaseModel):
    user_id: str
    name: str

class CampaignSchema(BaseModel):
    name: str
    description: str
    gameMaster: str
    players: List[PlayerCharacter]
    password: str
    join_code: str

class CampaignCreate(BaseModel):
    name: str
    description: str
    password: str

class CampaignJoinSchema(BaseModel):
    join_code: str
    password: str
    character_name: str

def  generate_join_code():
    alphanum = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphanum).upper() for _ in range(6))

def db_create_campaign(campaign: CampaignCreate, user_id: str):
    campaign_doc = {
        "name": campaign.name,
        "description": campaign.description,
        "gameMaster": user_id,
        "players": [],
        "password": hash_password(campaign.password),
        "join_code": generate_join_code()
    }

    created_campaign = campaign_collection.insert_one(campaign_doc)

    # push into the user document the info as well
    gm_doc = {
        "campaign_id": created_campaign.inserted_id,
        "character_name": "",
        "role": "gm"
    }
    user_collection.update_one({"_id": ObjectId(user_id)}, {"$push": {"campaigns": gm_doc}}, upsert=True)

    return campaign_doc, created_campaign.inserted_id


def db_join_campaign(campaign_info: CampaignJoinSchema, user_id: str):
    # FIRST GET THE CAMPAIGN BY JOIN CODE!
    campaign = campaign_collection.find_one({"join_code": campaign_info.join_code})

    campaign_doc = {
        "campaign_id" : campaign["_id"],
        "character_name" : campaign_info.character_name,
        "role": "player"
    }

    user_collection.update_one({"_id": ObjectId(user_id)}, {"$push": {"campaigns": campaign_doc}}, upsert=True)

    player_doc = {
        "players": user_id,
        "character_name": campaign_info.character_name,
    }

    campaign_collection.update_one({"_id": campaign["_id"]}, {"$push": {"players": player_doc}}, upsert=True)

    return {
        "campaign_id": campaign["_id"],
        "character_name": campaign_info.character_name,
    }