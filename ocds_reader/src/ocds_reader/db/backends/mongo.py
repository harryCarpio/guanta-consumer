import pymongo
import re
import os
from configparser import ConfigParser
from pymongo.server_api import ServerApi
import bson
import jsondiff

class MongoClient:

    def __init__(self):
        #Read db.ini file
        config_object = ConfigParser()
        current_directory = os.path.dirname(__file__)
        config_file = os.path.join(current_directory, 'config.ini')
        config_object.read(config_file)
        mongo_conn = config_object["MONGODB"]
        mongo_host = mongo_conn["host"]
        mongo_port = mongo_conn["port"]
        mongo_usr = mongo_conn["user"]
        mongo_psw = mongo_conn["passwd"]
        self.__mongo_db = mongo_conn["db"]
        uri = "mongodb+srv://"+mongo_usr+":"+mongo_psw+"@"+mongo_host+"/?retryWrites=true&w=majority&appName=AtlasApp"
        self.__connection = pymongo.MongoClient(uri, server_api=ServerApi('1'))

    def update_collection(self, collection_name, doc, filter, upsert):
        mongo_db = self.__connection[self.__mongo_db]
        collection = mongo_db[collection_name]
        collection.update_one(filter, {"$set": doc}, upsert=upsert)

    def insert_doc(self, collection_name, doc):
        mongo_db = self.__connection[self.__mongo_db]
        collection = mongo_db[collection_name]
        collection.insert_one(doc)

    def document_exist(self, collection_name, id):
        mongo_db = self.__connection[self.__mongo_db]
        collection = mongo_db[collection_name]
        doc = collection.find_one({"_id": id})
        return doc != None

    def is_document_updated(self, collection_name, id, new_doc):
        mongo_db = self.__connection[self.__mongo_db]
        collection = mongo_db[collection_name]
        old_doc = collection.find_one({"_id": id})
        return old_doc != new_doc
    
    def register_scd(self, collection_name, id, target_collection, change_detected):
        mongo_db = self.__connection[self.__mongo_db]
        collection = mongo_db[collection_name]
        doc = collection.find_one({"_id": id})
        doc["id"] = id
        doc["change_detected"] = change_detected
        doc["_id"] = bson.ObjectId()
        self.insert_doc(target_collection, doc)

    def register_scd_diff(self, collection_name, id, target_collection, new_doc, change_detected):
        mongo_db = self.__connection[self.__mongo_db]
        collection = mongo_db[collection_name]
        doc = collection.find_one({"_id": id})
        diff = jsondiff.diff(doc, new_doc, syntax='symmetric')
        diff["_id"] = bson.ObjectId()
        diff["change_detected"] = change_detected
        self.insert_doc(target_collection, diff)