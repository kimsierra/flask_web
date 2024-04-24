#mongodb local cocnnect
import pymongo
from pymongo import MongoClient
import bson


mongodb_url ='mongodb+srv://root:1234@mydb.1vno0ws.mongodb.net/?retryWrites=true&w=majority' # 로컬 할 때/ 클라우드할 때

class MONGODB:
    def __init__(self, mongodb_url, db_name):
        
        try:    
            self.client = MongoClient(mongodb_url)
            self.db = self.client[db_name]
            print("Connected successfully!!!")
        except:
            print("Could not connect to MongoDB")
 

# def get_db(client, db_name):
#     db = client[db_name]
#     return db

# def get_collection(db_name, collection_name): #SQL에서는 테이블에 해당하는 콜렉션
#     db = client[db_name]
#     collection = db[collection_name]
#     return collection

    def insert_data(self, collection, data):
       
        document = self.db[collection]
        try:
            rec_id1 = document.insert_one(data)
            print("Data inserted with record ids", rec_id1)
        except:
            print("Could not insert data")

    def find_data(self, collection,query={}):
        
        document = self.db[collection]
        try:
            cursor = document.find(query)
            #print(cursor)
            find_list=[]
            for record in cursor:
                find_list.append(record)
            return find_list # 조회한 것 리턴받기
        except:
            print("Could not find data")
    def update_data(self, collection, query, values ): #query:찾을거 new_values: 어떻게 바꿀지   
        document = self.db[collection]
        try:
            document.update_one(query, {"$set":values})
            print("Data updated successfully")
        except:
            print("Could not update data")
    def delete_data(self, collection, query):
        
        document = self.db[collection]
        try:
            document.delete_one(query)
            print("Data deleted successfully")
        except:
            print("Could not delete data")


if __name__ == "__main__":
   mongodb = MONGODB(mongodb_url, db_name='mytest')
   doc ={
       "username":"Gary3",
       "email":"3@naver.com",
       "password":"1234"
   }
   mongodb.insert_data(collection='mydoc',data=doc)
   query = {
        "email": "1@naver.com"
    }
   #find_list = mongodb.find_data(collection='mydoc',query=query)
   #print(find_list)
   query = {'_id':bson.ObjectId("6628646936ce2a0ff67daade")  }
   new_values = {"username":"HHH", "email":"2@naver.com", "address":"seoul"}
   #mongodb.update_data(collection='mydoc',query=query, values=new_values)
   #mongodb.delete_data(collection='mydoc', query=query)
   