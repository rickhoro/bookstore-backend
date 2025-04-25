from core.security import hash_password
from db.mongo import get_user_collection
import os

from models.user import Role, UserInDB

INITIAL_SUPERUSER_EMAIL = os.getenv("INITIAL_SUPERUSER_EMAIL")
INITIAL_SUPERUSER_PASS = os.getenv("INITIAL_SUPERUSER_PASS")

async def create_initial_user():
    users = get_user_collection()
    existing_superuser = await users.find_one({"email": INITIAL_SUPERUSER_EMAIL})
    if not existing_superuser:
        superuser_for_db = UserInDB(
            email  = INITIAL_SUPERUSER_EMAIL,
            password = "",
            hashed_password = hash_password(INITIAL_SUPERUSER_PASS),
            role = Role.superuser
        )

        await users.insert_one(superuser_for_db.model_dump())
        print("Superuser created with username: superadmin and password: supersecret")
