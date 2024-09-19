from .base_model import MyBaseModel


class SessionModel(MyBaseModel):
    _coll_name = "sessions"
    _custom_int64_fields = ["expired_at"]

    session_token: str = ""
    jwt_token: str = ""
    expired_at: int = 0
    user_id: str = 0  # same as created_by

class RefreshTokenModel(MyBaseModel):
    _coll_name: str = "refresh_tokens"
    _custom_int64_fields = ["expired_at"]

    refresh_token: str = ""
    expired_at: int = 0
    user_id: str = 0  # same as created_by