#mongodb local cocnnect
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb+srv://root:1234@mydb.1vno0ws.mongodb.net/?retryWrites=true&w=majority')

def connect_mongodb():
    try:
        client = MongoClient('mongodb+srv://root:1234@mydb.1vno0ws.mongodb.net/?retryWrites=true&w=majority') # 로컬 할 때/ 클라우드할 때
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")
    return client

def get_db(client, db_name):
    db = client[db_name]
    return db

def get_collection(db_name, collection_name): #SQL에서는 테이블에 해당하는 콜렉션
    db = client[db_name]
    collection = db[collection_name]
    return collection

def insert_data(data):
    client = MongoClient('mongodb+srv://root:1234@mydb.1vno0ws.mongodb.net/?retryWrites=true&w=majority')
    db = client['mytest']
    collection = db['mycollection']
    try:
        rec_id1 = collection.insert_one(data)
        print("Data inserted with record ids", rec_id1)
    except:
        print("Could not insert data")

def find_data(query={}):
    client = MongoClient('mongodb+srv://root:1234@mydb.1vno0ws.mongodb.net/?retryWrites=true&w=majority')
    db = client['mytest']
    collection = db['mycollection']
    try:
        cursor = collection.find(query)
        for record in cursor:
            print(record)
    except:
        print("Could not find data")

def update_data(collection, query, new_values):
    try:
        collection.update_one(query, new_values)
        print("Data updated successfully")
    except:
        print("Could not update data")

def delete_data(collection, query):
    try:
        collection.delete_one(query)
        print("Data deleted successfully")
    except:
        print("Could not delete data")

def main():
    client = connect_mongodb()
    db = get_db(client, 'test')
    collection = get_collection(db, 'test')
    data = {
        'name': 'John',
        'age': 25,
        'address': 'New York'
    }
    insert_data(collection, data)
    query = {'name': 'John'}
    find_data(collection, query)
    new_values = {"$set": {'name': 'Sam'}}
    update_data(collection, query, new_values)
    find_data(collection, query)
    delete_data(collection, query)
    find_data(collection, query)

if __name__ == "__main__":
    #connect_mongodb()
    #db = get_db(client, "mytest")
    # collection = get_collection("mytest", "mycollection")
    # print(collection)
    find_data()
    # insert_data({"city":"Seoul",
    #              "name":"ubion",
    #              "data":"Hello"})