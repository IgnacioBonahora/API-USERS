from fastapi import APIRouter,HTTPException
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema

router= APIRouter(prefix="/usersdb",
                    tags=["usersdb"],
                    responses={404: {"message": "no encontrado"}})

#entidad User


users_list =[]



@router.get("/")
async def users():
    return users_list


#path
@router.get("/{id}")
async def user(id: int):
    return serach_users(id)

#query
@router.get("/")
async def user(id: int):
    return serach_users(id)

@router.post("/", response_model=User, status_code=201)
async def user(user: User):
    # if type(serach_users(user.id)) == User:
    #     raise HTTPException(status_code=204,detail="el usuario ya existe")
    # else:
    #     users_list.append(user)

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = db_client.local.users.find_one({"_id": id})

    return user

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
                









def serach_users(id:int):
    users=filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        raise HTTPException(status_code=404,detail="el usuario no existe")
    




#documentaciones
#swagger: http://127.0.0.1:8000/docs
#redocly: http://127.0.0.1:8000/redoc


