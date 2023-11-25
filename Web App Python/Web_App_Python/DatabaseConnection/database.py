from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

databaseClient = MongoClient('mongodb://Group18User:Group18Password@172.178.120.69:27017/')
db = databaseClient['Group_18_Database']
collection = db['passenger_data']

try:
    # The ismaster command is cheap and does not require auth.
    databaseClient.admin.command('ismaster')
    print("Connection Successful!")
except ConnectionFailure:
    print("Server not available")
