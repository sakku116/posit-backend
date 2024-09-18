from domain.model.user_model import UserModel
from repository import user_repo
from utils import bcrypt as bcrypt_utils
from config.env import Env
import logging
from utils import helper

logger = logging.getLogger(__name__)


def seedUsers(user_repo: user_repo.UserRepo):
    logger.info("seeding users")
    if not Env.INITIAL_USER_USERNAME or not Env.INITIAL_USER_PASSWORD:
        logger.warning(
            "Env.INITIAL_USER_USERNAME or Env.INITIAL_USER_PASSWORD is not set"
        )
        return

    if not Env.INITIAL_USER_USERNAME.islower() or " " in Env.INITIAL_USER_USERNAME:
        raise Exception("Env.INITIAL_USER_USERNAME is not lowercase")

    time_now = helper.timeNow()
    user_list = [
        UserModel(
            id=helper.generateUUID(),
            created_at=time_now,
            username=Env.INITIAL_USER_USERNAME,
            password=bcrypt_utils.hashPassword(Env.INITIAL_USER_PASSWORD),
            fullname=Env.INITIAL_USER_USERNAME.replace("_", " ").capitalize(),
            email=f"{Env.INITIAL_USER_USERNAME}@example.com",
        )
    ]

    for user in user_list:
        logger.info(f"seeding user: {user.username}")
        existing_user = user_repo.get(username=user.username)
        if existing_user:
            logger.info(f"user {user.username} already exists")
            continue

        user_repo.create(user)

    logger.info("users seeded")
