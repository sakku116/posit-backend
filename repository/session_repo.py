from fastapi import Depends
from pymongo import ReturnDocument
from pymongo.database import Database
from domain.model import session_model
from core.logging import logger
from typing import Union

from config.mongodb import getMongoDB
import logging

class SessionRepo:
    def __init__(self, mongodb: Database = Depends(getMongoDB)):
        self.session_coll = mongodb[session_model.SessionModel()._coll_name]
        self.refresh_token_coll = mongodb[session_model.RefreshTokenModel()._coll_name]

    def create(self, data: session_model.SessionModel):
        self.session_coll.insert_one(data.model_dump())

    def get(self, id: str) -> Union[session_model.SessionModel, None]:
        session = self.session_coll.find_one({"id": id})
        return session_model.SessionModel(**session) if session else None