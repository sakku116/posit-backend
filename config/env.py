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

    JWT_EXP: int = int(os.getenv("JWT_EXP", 9)) # hours
    JWT_SECRET: str = os.getenv("JWT_SECRET", "secret")
    AES_SECRET: str = os.getenv("AES_SECRET", "secret")
    INTERNAL_TOKEN: str = os.getenv("INTERNAL_TOKEN", "")
    INITIAL_USER_USERNAME: str = os.getenv("INITIAL_USER_USERNAME", None)
    INITIAL_USER_PASSWORD: str = os.getenv("INITIAL_USER_PASSWORD", None)