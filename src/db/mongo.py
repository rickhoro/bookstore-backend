from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.collection import Collection
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()  # Load variables from .env

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
MONGO_DB = os.getenv("MONGO_DB", "bookstore")
BS_APP_NAME = os.getenv("BS_APP_NAME")
encoded_password = quote_plus(MONGO_PASS)

print(encoded_password)

# Construct MongoDB Atlas URI
MONGO_URI = (
    f"mongodb+srv://{MONGO_USER}:{encoded_password}@{MONGO_CLUSTER}/"
    f"?retryWrites=true&w=majority&appName={BS_APP_NAME}"
)
print(f"MONGO_URI={MONGO_URI}")

client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None
user_collection: Collection | None = None

def get_user_collection() -> Collection:
    return db["users"]

async def connect_to_mongo():
    global client, db, user_collection
    client = AsyncIOMotorClient(MONGO_URI)
    print(await client.list_database_names())
    try:
        db = client[MONGO_DB]  # Default to the specified database in the URI
        print("✅ Connected to MongoDB")
        print(await client.list_database_names())
        user_collection = db["users"]  # Initialize the user collection
        print(f"user_collection type={type(user_collection)}, collection={user_collection}");
        print(f"databases={await client.list_database_names()}")
    except ConnectionError as e:
        print(f"Failed to connect to database: {e}")
        raise


async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("MongoDB connection closed")


def get_user_collection():
    if db is None:
        raise RuntimeError("DB not initialized yet")
    return db["users"]