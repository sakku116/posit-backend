from fastapi import Depends
from pymongo import ReturnDocument
from pymongo.database import Database
from domain.model import session_model

from config.mongodb import getMongoDB
import logging

logger = logging.getLogger(__name__)

class SessionRepo:
    def __init__(self, mongodb: Database = Depends(getMongoDB)):
        self.session_coll = mongodb[session_model.SessionModel._coll_name]
        self.refresh_token_coll = mongodb[session_model.RefreshTokenModel._coll_name]
