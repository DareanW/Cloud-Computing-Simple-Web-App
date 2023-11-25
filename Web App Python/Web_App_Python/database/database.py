from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

client = MongoClient('mongodb://Group18User:Group18Password@172.178.120.69:27017/')
db = client['Group_18_Database']
collection = db['passenger_data']

try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("Connection Successful!")
except ConnectionFailure:
    print("Server not available")
