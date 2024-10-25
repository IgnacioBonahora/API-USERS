from pymongo import MongoClient


#bd local
# db_client = MongoClient("mongodb://localhost:27017/").local

#bd remota
db_client = MongoClient(
    "mongodb+srv://admin:<contraseña>@cluster0.cshdu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test