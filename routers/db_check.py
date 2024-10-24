from fastapi import APIRouter, HTTPException
from pymongo import MongoClient

router = APIRouter()

# Conexión a MongoDB (ajusta la URI si es necesario)
db_client = MongoClient("mongodb://localhost:27017/")

@router.get("/check-db-connection")
async def check_db_connection():
    try:
        # Intentar acceder a la base de datos 'local' y listar colecciones
        db = db_client.local
        collections = db.list_collection_names()
        return {"message": "Conexión exitosa a MongoDB", "collections": collections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error conectándose a MongoDB: {e}")
