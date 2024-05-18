
import pymongo


class db:
    client = pymongo.MongoClient("localhost:27017")
    database = client.get_database("Tournament")

    @classmethod
    def insert(cls,collection : str,insertion : dict | list[dict]) -> None:
        collection = cls.database.get_collection(collection)
        
        if type(insertion)==dict:
            collection.insert_one(insertion)
        elif type(insertion)==list:
            collection.inert_many(insertion)

    @classmethod
    def find_all(cls,collection : str,*,query :dict={})-> list[dict]:
        collection = cls.database.get_collection(collection)

        out = collection.find(query)
        return [*out]


    @classmethod
    def find_one(cls,collection :str,*,query :dict) -> dict:
        collection = cls.database.get_collection(collection)
        
        return collection.find_one(query) #type:ignore
        
    @classmethod
    def update_one(cls,collection,*,query :dict,update_dict : dict):
        collection = cls.database.get_collection(collection)
        collection.update_one(query, {"$set":update_dict})

    @classmethod
    def get_distinct_values(cls,collection:str,key:str) -> list:
        collection= cls.database.get_collection(collection)
        return collection.distinct(key)
        