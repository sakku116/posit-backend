from .base_model import MyBaseModel, _MyBaseModel_Index
from typing import Literal


class UserModel(MyBaseModel):
    _coll_name: str = "users"
    _custom_indexes: list[_MyBaseModel_Index] = [
        _MyBaseModel_Index(keys=[("username", 1)], unique=True),
    ]

    username: str = ""
    password: str = ""
    fullname: str = ""
    email: str = ""
