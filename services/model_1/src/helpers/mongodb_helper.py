#!/bin/env python3

# Python version: 3.8.3
# Author: Liam Ling
# Contact: liam_ling@sfu.ca
# File name: mongodb_helper.py
# Description:
"""Helper MongoDB helper
"""

import logging

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

logger = logging.getLogger(__name__)

def get_client(host:str="localhost", port:int=27017):
    try:
        client = MongoClient()
        return client
    except ConnectionFailure:
        logger.error(f"Error in creating connection to client")

def get_collection(_client, _database:str, _collection:str):
    if _client != None and _database != None and _collection != None:
        try:
            database = _client[_database]
            collection = database[_collection]
            return collection
        except Exception as e:
            logger.error(f"Error in getting collection: {e}")
    else:
        logger.error(f"Some parameters are None: {_client}, {_database}, {_collection}")

def insert_single_doc(_client, _database:str, _collection:str, data=None):
    if data != None:
        target_collection = get_collection(_client, _database, _collection)
        obj_id = target_collection.insert_one(data)
        return obj_id
    else:
        logger.error(f"Data is None")

