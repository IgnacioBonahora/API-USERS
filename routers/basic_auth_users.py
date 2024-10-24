from fastapi import APIRouter,Depends,HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool

class UserDB(User):
    password: str

users_db = {
    "nacho":{
        "username": "nacho",
        "full_name": "ignacio Bonahora",
        "email": "ignacio@gmail.com",
        "disable": False,
        "password": "123456"
    },
    "nacho2":{
        "username": "nacho2",
        "full_name": "ignacio Bonahora 2",
        "email": "ignacio2@gmail.com",
        "disable": True,
        "password": "654321"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="credenciales de autenticacion invaldidas",
                            headers={"WWW-Authenticate":"Bearer"})
    if user.disable:
                raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo")
    return user
    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400,detail="usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=400,detail="la contaseña no es correcta")
    
    return{"access_token":user.username,"token_tipe":"bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user


