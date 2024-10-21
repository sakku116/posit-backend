from fastapi import Depends
from pymongo import ReturnDocument
from pymongo.database import Database
from domain.model import session_model
from core.logging import logger

from config.mongodb import getMongoDB
import logging

class SessionRepo:
    def __init__(self, mongodb: Database = Depends(getMongoDB)):
        self.session_coll = mongodb[session_model.SessionModel()._coll_name]
        self.refresh_token_coll = mongodb[session_model.RefreshTokenModel()._coll_name]

    def create(self, data: session_model.SessionModel):
        self.session_coll.insert_one(data.model_dump())