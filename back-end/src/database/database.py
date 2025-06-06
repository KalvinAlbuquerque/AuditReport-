from pymongo import MongoClient
from typing import Any, Dict, List
from bson.objectid import ObjectId # <-- ADICIONE ESTA IMPORTAÇÃO

class Database:
    def __init__(self, db_name: str = "database"):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]

    def insert_one(self, collection_name: str, data: Dict[str, Any]):
        return self.db[collection_name].insert_one(data)

    def insert_many(self, collection_name: str, data_list: List[Dict[str, Any]]):
        return self.db[collection_name].insert_many(data_list)

    def find_one(self, collection_name: str, query: Dict[str, Any]):
        return self.db[collection_name].find_one(query)

    def find(self, collection_name: str, query: Dict[str, Any] = {}):
        return list(self.db[collection_name].find(query))

    def update_one(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]):
        return self.db[collection_name].update_one(query, {"$set": update})

    def delete_one(self, collection_name: str, query: Dict[str, Any]):
        return self.db[collection_name].delete_one(query)

    def delete_many(self, collection_name: str, query: Dict[str, Any]):
        return self.db[collection_name].delete_many(query)

    def count_documents(self, collection_name: str, query: Dict[str, Any] = {}):
        return self.db[collection_name].count_documents(query)

    def close(self):
        self.client.close()

    # --- ADICIONE ESTE NOVO MÉTODO ---
    def get_object_id(self, id_string: str) -> ObjectId:
        """Converte uma string de ID em um ObjectId do MongoDB."""
        return ObjectId(id_string)
    # ---------------------------------


# -----------------------
# Exemplos de uso
# -----------------------

if __name__ == "__main__":

    db = Database()

    # 1. Inserir um documento
    usuario_id = db.insert_one("usuarios", {"nome": "Alice", "idade": 25})
    print("ID inserido:", usuario_id)

    # 2. Inserir vários documentos
    ids = db.insert_many("usuarios", [
        {"nome": "Bob", "idade": 30},
        {"nome": "Carol", "idade": 35}
    ])
    print("IDs inseridos:", ids)

    # 3. Buscar um usuário
    usuario = db.find_one("usuarios", {"nome": "Alice"})
    print("Usuário encontrado:", usuario)

    # 4. Buscar todos os usuários
    todos = db.find("usuarios")
    print("Todos os usuários:")
    for u in todos:
        print(u)

    # 5. Atualizar um usuário
    if usuario:
        result = db.update_one("usuarios", {"_id": usuario["_id"]}, {"idade": 26})
        print("Documentos modificados:", result.modified_count)

    # 6. Contar documentos
    quantidade = db.count_documents("usuarios")
    print("Total de usuários:", quantidade)

    # 7. Deletar um usuário (agora com o ID convertido)
    if usuario and "_id" in usuario: # Garantindo que o _id existe
        result = db.delete_one("usuarios", {"_id": usuario["_id"]})
        print("Documentos deletados:", result.deleted_count)

    # 8. Deletar vários
    result = db.delete_many("usuarios", {"nome": {"$in": ["Bob", "Carol"]}})
    print("Vários deletados:", result.deleted_count)

    db.close()