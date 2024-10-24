from fastapi import APIRouter,HTTPException
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema , users_schema
from bson import ObjectId

router= APIRouter(prefix="/userdb",
                    tags=["userdb"],
                    responses={404: {"message": "no encontrado"}})

#entidad User


users_list =[]



@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.local.users.find())


#path
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))

#query
@router.get("/")
async def user(id: str):
    return search_user("_id",   ObjectId(id))

@router.post("/", response_model=User, status_code=201)
async def user(user: User):
    existing_user = search_user("email", user.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="El usuario ya existe")

    user_dict = dict(user)
    del user_dict["id"]  # Asegúrate de que este campo no esté en el diccionario

    id = db_client.local.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))

    return User(**new_user)


@router.put("/")
async def user(user: User):
    found = False
    for index, saved_users in enumerate(users_list):
        if saved_users.id == user.id :
            users_list[index]= user
            found = True
    if found == False:
        raise HTTPException(status_code=204,detail="el usuario no se modifico")
    else:
        return user

@router.delete("/{id}")
async def user(id:int):
        found=False
        for index, saved_users in enumerate(users_list):
            if saved_users.id == id :
                del users_list[index]
                found=True

        if not found:
            raise HTTPException(status_code=404,detail="el usuario no se elimino")





def search_user(field: str, key):
    user = db_client.local.users.find_one({field: key})
    if user:
        return user_schema(user)  # Devuelve el esquema del usuario si existe
    return None  # Devuelve None si no se encontró el usuario









#documentaciones
#swagger: http://127.0.0.1:8000/docs
#redocly: http://127.0.0.1:8000/redoc


