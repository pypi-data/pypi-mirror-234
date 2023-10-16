import sys
import traceback

from bson.binary import Binary as BsonBinary
from pymongo import InsertOne, MongoClient, UpdateMany, UpdateOne


class MongoCL:
    def __init__(self, uri=None):

        self.cl = MongoClient(uri)

    def batchPut(self, puts=[], dbName="vcg", tableName=None):
        actions = []

        for put in puts:
            try:
                action = InsertOne(put)
                actions.append(action)

            except BaseException as e:
                print("put to db  error:%s" % str(e))
                print("-" * 60)
                traceback.print_exc(file=sys.stdout)
                print("-" * 60)
        self.cl[dbName][tableName].bulk_write(actions)

    def createIndex(
        self,
        dbName="vcg",
        tableName=None,
        fieldName=None,
        unique=True,
        background=False,
    ):
        self.cl[dbName][tableName].create_index(
            fieldName, unique=unique, background=background
        )

    def dropTable(self, dbName="vcg", tableName=None):
        try:
            self.cl[dbName][tableName].drop()
        except BaseException as e:
            print("put to db  error:%s" % str(e))
            print("-" * 60)
            traceback.print_exc(file=sys.stdout)
            print("-" * 60)


class HbaseCL:
    def __init__(self, uri=None):
        host = uri.split(":")[0]
        port = int(uri.split(":")[1])
        # self.cl = happybase.Connection(host=host, port=port, timeout=None)

    def batchPut(self, puts=[], dbName="vcg", tableName=None, idName="c0:imageId"):
        """

        :param puts:  {'c0:imageId':'12323434','c1:features':'1.0,2.0'......}
        :param dbName:
        :param tableName:
        :param idName:
        :return:
        """
        table = self.cl.table(tableName)

        batchOps = table.batch()

        for put in puts:
            try:
                columns = {}
                for key, value in put.items():
                    # key_ = key.encode()
                    # value_ = value.encode()
                    columns[key] = value

                batchOps.put(put[idName].encode(), columns)

            except ValueError as e:

                print("put to hbase  error:%s" % str(e))
                print("-" * 60)
                traceback.print_exc(file=sys.stdout)
                print("-" * 60)

        batchOps.send()

    def scan(self, tableName=None, columns=None):
        """

        :param tableName:
        :param columns:  ['c0:column1','c1:column1'...]
        :return: datas: (rowKey,columns (dic))
        """
        table = self.cl.table(tableName)

        datas = table.scan(columns=columns)
        return datas


dbsMapping = {}


def batchPut(params={}):

    dbType = params.get("dbType", "mongo")
    print("batchPut, dbType: %s,  tableName: %s" % (dbType, params["tableName"]))

    if dbType == "mongo":
        print("start to batchPut to mongodb")
        uri = "mongodb://zhaoyufei:vcgjasstion@gpu0.dev.yufei.com:27017/vcg?authMechanism=SCRAM-SHA-1"

        mongoCL = dbsMapping.get(uri)
        if mongoCL == None:
            mongoCL = MongoCL(uri=uri)
            dbsMapping[uri] = mongoCL
        puts = params["puts"]
        tableName = params["tableName"]
        mongoCL.batchPut(puts=puts, tableName=tableName)
    if dbType == "hbase":
        print("start to batchPut to hbase")
        uri = "gpu0.dev.yufei.com:9999"

        hbaseCL = dbsMapping.get(uri)
        if hbaseCL == None:
            hbaseCL = HbaseCL(uri=uri)
            dbsMapping[uri] = hbaseCL
        idName = params.get("idName", "c0:imageId")
        # rowKey value 就是从puts获取idName的value
        puts = params["puts"]
        tableName = params["tableName"]
        hbaseCL.batchPut(puts=puts, tableName=tableName, idName=idName)
