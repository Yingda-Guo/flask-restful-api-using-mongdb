import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27018/")

mydb = myclient["testdb"]
print(myclient.list_database_names())