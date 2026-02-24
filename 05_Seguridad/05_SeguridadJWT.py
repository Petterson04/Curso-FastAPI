from datetime import datetime, timedelta, timezone
import jwt
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

# CONFIG (En un proyecto real esto se irar a variables de entorno/settings)

SECRET_KEY="e60b640c5e4b893e8fec40d72df469a09cca0bcb239f5f848951f7a1c3af98e8"
algorithm="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Hasehar contraseñas
pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password (plain_password: str, Hash_password: str):
    return pwd_context.verify(plain_password, Hash_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

#FAKE DB
ake_users_db= {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "john@example.com",
        "hashed_password": get_password_hash("secret"),
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": get_password_hash("secret2"),
        "disabled": True,
    },
}

#Models  
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None
    email: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str
    
#AUth HELPERS
def get_user(db: dict, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(fakeDb: dict, username: str, password: str):
    user = get_user(fakeDb, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode= data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    enconded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=algorithm)
    return enconded_jwt

#FASTAPI 
app = FastAPI()
oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credencials_exceptions = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[algorithm])
        username = payload.get("sub")
        if username is None:
            raise credencials_exceptions
        token_data = TokenData(username= username)
    except InvalidTokenError:
        raise credencials_exceptions
    if token_data.username is None:
        raise credencials_exceptions
    user = get_user(ake_users_db, username= token_data.username)
    if user is None:
        raise credencials_exceptions
    return user 

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user 

#ROUTES

@app.post("/token", response_model= Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user= authenticate_user(ake_users_db, form_data.username, form_data.password)
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
            )
    acess_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    acces_token = create_access_token(data={"sub": user.username}, expires_delta=acess_token_expire)
    if acces_token is None:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
            )
    return Token(access_token=acces_token, token_type="bearer")
    
@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user