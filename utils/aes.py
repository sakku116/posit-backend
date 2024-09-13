from config.env import Env
from AesEverywhere import aes256

def encrypt(raw: str):
    return aes256.encrypt(raw, Env.AES_SECRET).decode("utf-8")

def decrypt(enc):
    return aes256.decrypt(enc, Env.AES_SECRET).decode("utf-8")