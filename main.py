from typing import Union
from fastapi import FastAPI
from routers import products,users, basic_auth_users, jwt_auth_users ,users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#routers
app.include_router(products.router)
app.include_router(users.router)

app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/")
async def root():
    return {"Hello sasWorld"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": 5, "q": "hamburguesa"}

@app.get("/nosotros")
async def read():
    return {"holaaa"}

@app.get("/url")
async def read():
    return {"url_curso":"https//mouredev.com/python"}





#iniciar server: uvicorn main:app --reload
#detener server: CTRL+C

#documentaciones
#swagger: http://127.0.0.1:8000/docs
#redocly: http://127.0.0.1:8000/redoc