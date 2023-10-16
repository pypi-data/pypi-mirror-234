import time
import unittest

from loguru import logger as logger1

from souJpg.comm.ops.ops import OpsClient


class OpsClientTestCase(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName=methodName)

        self.esClient = OpsClient()
        self.indexMappingMap = {}
        indexName = "image_search"
        indexMapping = {
            "settings": {
                "number_of_shards": 3,
                "number_of_replicas": 0,
                "refresh_interval": "1s",
                "analysis": {
                    "analyzer": {
                        "payload_delimiter": {
                            "tokenizer": "whitespace",
                            "filter": ["delimited_payload"],
                        }
                    }
                },
            },
            "mappings": {
                "_source": {"excludes": ["opq_features"]},
                "properties": {
                    "kwPayloads": {
                        "type": "text",
                        "term_vector": "with_positions_payloads",
                        "analyzer": "payload_delimiter",
                    },
                    "quality": {"type": "float"},
                    "opq_features": {
                        "type": "text",
                        "analyzer": "whitespace",  # 'store':False
                    },
                    "imageId": {
                        "type": "keyword",
                        "index": True,  # 'store': True,
                        "doc_values": False,
                    },
                },
            },
        }
        self.indexMappingMap[indexName] = indexMapping

    def reCreateIndexAndPopulate(self, indexName=None):
        if self.esClient.client.indices.exists(indexName):
            self.esClient.client.indices.delete(index=indexName)
        # index settings
        settings = self.indexMappingMap.get(indexName)
        # create index
        self.esClient.client.indices.create(index=indexName, body=settings)
        op_type = "index"
        docs = []
        i = 1
        action = {}
        action["_id"] = i
        action["imageId"] = str(i)
        action["opq_features"] = "23_1 45_2 56_2"
        action["kwPayloads"] = "狗|0.9 猫|0.4"
        docs.append(action)

        i = 2
        action = {}

        action["_id"] = i
        action["imageId"] = str(i)
        action["opq_features"] = "23_1 45_2 56_2"
        action["kwPayloads"] = "汽车|0.9 猫|0.4"
        docs.append(action)

        i = 3
        action = {}

        action["_id"] = i
        action["imageId"] = str(i)
        action["opq_features"] = "23_1 45_2 56_2"
        action["kwPayloads"] = "狗|0.9 游泳|0.4"
        docs.append(action)

        i = 4
        action = {}

        action["_id"] = i
        action["imageId"] = str(i)
        action["opq_features"] = "23_1 45_2 56_2"
        action["kwPayloads"] = "人|0.9 拳击|0.4"
        docs.append(action)

        i = 5
        action = {}

        action["_id"] = i
        action["imageId"] = str(i)
        action["opq_features"] = "23_1 45_2 56_2"
        action["kwPayloads"] = ""
        docs.append(action)

        self.esClient.batchUpdate(indexName=indexName, op_type=op_type, docs=docs)

    def test_updateByQuery(self):
        indexName = "image_search"
        updatedField = "kwPayloads"
        updatedValue = "人|0.9 拳击|0.4 健身房|0.32"
        queryField = "imageId"
        queryValue = "5"
        # updatedBody = {"script": {"source": "ctx._source.%s='%s'" % (updatedField,updatedValue), "lang": "painless"},
        #                "query": {"term": {"%s" % (queryField): "%s" % (queryValue)}}}
        self.reCreateIndexAndPopulate(indexName=indexName)
        time.sleep(2)
        # update imageId: 4  , kwPayloads: 人|0.9 拳击|0.4  -> 人|0.9 拳击|0.4 健身房|0.1
        result = self.esClient.updateByQuery(
            indexName=indexName,
            updatedValue=updatedValue,
            updatedField=updatedField,
            queryValue=queryValue,
            queryField=queryField,
        )
        # result = self.esClient.updateByQuery(index=indexName, updatedBody=updatedBody)
        logger1.info(result)

    def test_batchUpdate(self):
        indexName = "image_search"
        op_type = "update"
        # op_type = 'index'
        self.reCreateIndexAndPopulate(indexName=indexName)

        docs = []
        for i in range(5):
            doc = {}
            doc["kwPayloads"] = "汽车|0.9 猫|0.4"
            doc["_id"] = str(i)
            docs.append(doc)

        self.esClient.batchUpdate(indexName=indexName, op_type=op_type, docs=docs)

    def test_msearch(self):
        indexName = "image_search"
        imageIds = ["1", "2", "4", "123"]
        kwPayloadses = self.esClient.getKwPayloadsByImageIds(
            indexName=indexName, imageIds=imageIds
        )
        for imageId, kwPayloads in zip(imageIds, kwPayloadses):
            logger1.info(imageId)
            logger1.info(
                kwPayloads
            )  # indexName = 'image_search'  # self.reCreateIndexAndPopulate(indexName=indexName)  # time.sleep(1)  #  #  # search_arr = []  # # req_head  # search_arr.append({'index': indexName})  # # req_body  # search_arr.append({"query": {"match": {"imageId": "1"}}, 'from': 0, 'size': 1})  #  # # req_head  # search_arr.append({'index': indexName})  # # req_body  # search_arr.append({"query": {"match": {"imageId": "2"}}, 'from': 0, 'size': 1})  # search_arr.append({'index': indexName})  # # req_body  # search_arr.append({"query": {"match": {"imageId": "20"}}, 'from': 0, 'size': 1})  #  # request = ''  # for each in search_arr:  #     request += '%s \n' % json.dumps(each)  #  # result=self.esClient.client.msearch(index=indexName,body=request)  # logger1.info(result)  # docs=[]  # for response in result.get('responses',[]):  #     matchedDocs=response.get('hits',{}).get('hits',[])  #     if len(matchedDocs)==0:  #         docs.append({})  #     else:  #         for doc in matchedDocs:  #             docs.append(doc)  # logger1.info(docs)

    def test_updateImageKwPayloads(self):
        indexName = "image_search"
        self.reCreateIndexAndPopulate(indexName=indexName)
        time.sleep(2)
        batches = []
        # 汽车|0.9 猫|0.4
        batches.append(("2", ""))
        batches.append(("5", "兔子|0.02"))
        batches.append(("1", "兔子|0.03"))
        self.esClient.updateImageKwPayloads(batches=batches, indexName=indexName)

    def test_pgSearch(self):
        indexName = "autotags_5m_fb_32_16_images"
        kwIds = ["621"]
        pageSize = 100
        pageNum = 100
        docs = self.esClient.pgQueryImagesByKwIds(
            indexName=indexName, kwIds=kwIds, pageSize=pageSize, pageNum=pageNum
        )
        logger1.debug(docs)
        for doc in docs:
            logger1.info(doc["_source"])


if __name__ == "__main__":
    unittest.main()
