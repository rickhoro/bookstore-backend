
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

password = "myeasypwd"
encoded_password = quote_plus(password)

print(encoded_password)
uri = f"mongodb+srv://rickhoro:{encoded_password}@test-cluster-0.spfzp.mongodb.net/?retryWrites=true&w=majority&appName=test-cluster-0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)




# from pymongo import MongoClient
# from urllib.parse import quote_plus

# encoded_password = quote_plus(password)

# print(encoded_password)


# print("Testing mongo Atlas connection")
# client = MongoClient(f"mongodb+srv://rickhoro:{encoded_password}@test-cluster-0.spfzp.mongodb.net/?retryWrites=true&w=majority")
# print(client.list_database_names())
