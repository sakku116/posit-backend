from .base_model import MyBaseModel, _MyBaseModel_Index
from typing import Literal


class UserModel(MyBaseModel):
    _coll_name: str = "users"
    _custom_indexes: list[_MyBaseModel_Index] = [
        _MyBaseModel_Index(keys=[("username", 1)], unique=True),
    ]
    _custom_int64_fields: list[str] = ["last_active"]

    username: str = ""
    password: str = ""
    fullname: str = ""
    email: str = ""
    banned: bool = False
    last_active: int = 0
