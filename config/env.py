from dataclasses import dataclass
import os
from utils.helper import parseBool

@dataclass(frozen=True)
class Env:
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    PRODUCTION: bool = parseBool(os.getenv("PRODUCTION", "false"))
    DEBUG: bool = parseBool(os.getenv("DEBUG", "false"))
    RELOAD: bool = parseBool(os.getenv("RELOAD", "false"))
    TZ: str = os.getenv("TZ", "Asia/Jakarta")

    TOKEN_EXP_HOURS: int = os.getenv("TOKEN_EXP_HOURS", 2)
    REFRESH_TOKEN_EXP_HOURS: int = int(os.getenv("REFRESH_TOKEN_EXP", 24))
    JWT_SECRET: str = os.getenv("JWT_SECRET", "secret")
    AES_SECRET: str = os.getenv("AES_SECRET", "secret")
    INTERNAL_TOKEN: str = os.getenv("INTERNAL_TOKEN", "")
    INITIAL_USER_USERNAME: str = os.getenv("INITIAL_USER_USERNAME", None)
    INITIAL_USER_PASSWORD: str = os.getenv("INITIAL_USER_PASSWORD", None)

    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_NAME: str = os.getenv("MONGODB_NAME", "posit_db")