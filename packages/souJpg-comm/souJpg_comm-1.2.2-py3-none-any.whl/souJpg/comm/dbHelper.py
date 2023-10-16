import sys
import threading
import traceback
from datetime import datetime

from bson.binary import Binary as BsonBinary
from loguru import logger as logger1
from pymongo import InsertOne, MongoClient, UpdateMany, UpdateOne

from souJpg import gcf

dbType2CollectionMap = {}
connection_lock = threading.Lock()


def createMongoDBConnection(dbType=None):
    global dbType2CollectionMap

    # check if connection for this dbType already exists
    if dbType in dbType2CollectionMap:
        return dbType2CollectionMap[dbType]

    # acquire lock to create new connection
    connection_lock.acquire()
    try:
        # double-check if connection was created by another thread while waiting for lock
        if dbType in dbType2CollectionMap:
            return dbType2CollectionMap[dbType]

        # create new connection and store in dbType2CollectionMap
        uri = gcf.dbURIMapping.get(dbType)
        dbName = uri.split("=")[1]
        client = MongoClient(
            uri,
            minPoolSize=10,
            maxPoolSize=100,
            maxIdleTimeMS=100000,
            connectTimeoutMS=30000,
            waitQueueTimeoutMS=20000,
            socketTimeoutMS=30000,
            compressors="zstd",
        )
        dbConnection = client[dbName]
        dbType2CollectionMap[dbType] = dbConnection
        return dbConnection

    finally:
        # release lock
        connection_lock.release()
