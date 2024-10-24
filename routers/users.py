from fastapi import APIRouter,HTTPException
from pydantic import BaseModel #capacidad de crear una entidad

router= APIRouter(prefix="/users",
                    tags=["users"],
                    responses={404: {"message": "no encontrado"}})

#entidad User
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list =[User(id=1,name= "ignacio",surname= "bonahora",url="https//bonahoraigna.com",age=21),
        User(id=2,name="juansito",surname= "azucarero",url="https//boesa.com",age=21),
        User(id=3,name="pedro",surname= "ludenia",url="https//bpeteris.com",age=42),
        User(id=4,name="pipo",surname= "suaso",url="https//bpeteris.com",age=22)]

@router.get("/usersjson")
async def usersjson():
    return [{"id": 1,"name":"ignacio","surname":"bonahora","url":"https//bonahoraigna.com","age": 21},
            {"id": 2,"name":"juansito","surname":"azucarero","url":"https//boesa.com","age": 11},
            {"id": 3,"name":"pedro","surname":"ludenia","url":"https//bpeteris.com","age": 42}]

@router.get("/")
async def users():
    return users_list


#path
@router.get("/user/{id}")
async def user(id: int):
    return serach_users(id)

#query
@router.get("/user/")
async def user(id: int):
    return serach_users(id)

@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(serach_users(user.id)) == User:
        raise HTTPException(status_code=204,detail="el usuario ya existe")
    else:
        users_list.append(user)
        return user

@router.put("/user/")
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
    
@router.delete("/user/{id}")
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


