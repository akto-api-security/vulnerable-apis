from pymongo import MongoClient
from django.conf import settings

# Establish a connection to the MongoDB database
mongo_db_settings = settings.DATABASES['mongo']
mongo_client = MongoClient(mongo_db_settings['CLIENT']['host'])
db = mongo_client[mongo_db_settings['NAME']]

