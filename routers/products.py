from fastapi import APIRouter

router = APIRouter(prefix="/products",#prefijo
                    tags=["products"],#tag para agrupar en la documentacion
                    responses={404: {"message": "no encontrado"}})

products_list =["producto 1","producto 2","producto 3","producto 4","producto 5"]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return products_list[id]
