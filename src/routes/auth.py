from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm
from jose import JWTError
from models.user import UserCreate, UserInDB, UserOut, Token
from pymongo.collection import Collection
from db.mongo import get_user_collection
from core.security import verify_password, hash_password, create_access_token, decode_access_token
from bson.objectid import ObjectId

router = APIRouter()

bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), users: Collection = Depends(get_user_collection)
):
    token = credentials.credentials
    try:
        email = decode_access_token(token)
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await users.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, users: Collection = Depends(get_user_collection)):
    result = await users.find_one({"email": user.email})
    if result:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_in_db = UserInDB(
        email = user.email,
        hashed_password = hash_password(user.password),
        password = ""
    )
    await users.insert_one(user_in_db)
    return {"email": user.email}


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), users: Collection = Depends(get_user_collection)):
    # form_data.username actually contains the user's email address because OAuth2PasswordRequestForm just names 
    #   it that way.
    user = await users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
async def get_me(user: str = Depends(get_current_user)):
    return {"email": user["email"]}


