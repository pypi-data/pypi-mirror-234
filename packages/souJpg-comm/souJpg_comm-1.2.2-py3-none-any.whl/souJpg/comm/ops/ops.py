from __future__ import absolute_import, division, print_function

import json
import sys
import traceback

import shortuuid
from loguru import logger as logger1
from opensearchpy import OpenSearch, helpers


class OpsClient:
    def __init__(self, params={}):
        self.params = params
        host = self.params.get("esHost", "gpu0.dev.yufei.com")
        port = self.params.get("esPort", 9200)
        self.client = OpenSearch([{"host": host, "port": port}])

    def buildIndex(self, indexName=None, settings=None):
        if self.client.indices.exists(indexName):
            self.client.indices.delete(index=indexName)
        self.client.indices.create(index=indexName, body=settings)

    def updateByQuery(
        self,
        indexName=None,
        updatedField=None,
        updatedValue=None,
        queryField=None,
        queryValue=None,
    ):
        """
        update by a given query  beside _id query
        use http request
        _update_by_query



        :return:
        """

        # updatedBody = {"script": {"source": "ctx._source.%s='%s'" % (updatedField, updatedValue), "lang": "painless"},
        #                "query": {"term": {"%s" % (queryField): "%s" % (queryValue)}}}
        updatedBody = {
            "script": {
                "source": "ctx._source.%s=params.updatedValue" % (updatedField),
                "lang": "painless",
                "params": {"updatedValue": updatedValue},
            },
            "query": {"term": {"%s" % (queryField): "%s" % (queryValue)}},
        }
        logger1.debug(updatedBody)
        result = self.client.update_by_query(
            index=indexName, body=updatedBody
        )
        logger1.debug(result)

        return result

    def batchUpdate(self, indexName=None, op_type=None, docs=None):
        """ """
        assert op_type in ["update", "index"]
        if docs is None or len(docs) == 0:
            logger1.warning("you try to index or update empty documents")

        baseInfo = {}
        actions = []
        if op_type == "index":
            baseInfo["_op_type"] = op_type
            baseInfo["_index"] = indexName
            baseInfo["_type"] = "_doc"

            for doc in docs:
                action = {}
                action.update(baseInfo)
                action.update(doc)
                logger1.debug(action)
                actions.append(action)
        elif op_type == "update":
            baseInfo["_op_type"] = op_type
            baseInfo["_index"] = indexName
            baseInfo["_type"] = "_doc"
            baseInfo["doc_as_upsert"] = "true"

            for doc in docs:
                action = {}

                id = doc.pop("_id")
                action["_id"] = id
                action["doc"] = doc
                action.update(baseInfo)

                logger1.debug(action)
                actions.append(action)
        result = helpers.bulk(self.client, actions)
        logger1.info(result)

        return result

    def batchDelete(self, actions=[]):
        """
        action = {'_op_type': 'delete', '_index': indexName, '_type': '_doc', '_id': id}
        :return:
        """
        result = helpers.bulk(self.client, actions)
        logger1.info(result)

        return result

    def pgSearch(self, indexName=None, query=None):
        items = []
        lastScore = None
        """
        pagation use search_after
        query:
        :return:
        _score and imageId
        """
        result = self.client.search(body=query, index=indexName)
        logger1.debug(result)
        return (items, lastScore)

    def getKwPayloadsByImageIds(self, indexName=None, imageIds=None):
        search_arr = []
        kwPayloads = []

        for imageId in imageIds:
            # req_head
            search_arr.append({"index": indexName})
            # req_body
            search_arr.append(
                {"query": {"match": {"imageId": "%s" % imageId}}, "from": 0, "size": 1}
            )
        request = ""
        for each in search_arr:
            request += "%s \n" % json.dumps(each)

        result = self.client.msearch(index=indexName, body=request)
        logger1.debug(result)
        docs = []
        for response in result.get("responses", []):
            matchedDocs = response.get("hits", {}).get("hits", [])
            if len(matchedDocs) == 0:
                docs.append({})
            else:
                for doc in matchedDocs:
                    docs.append(doc)
        logger1.debug(docs)
        for doc in docs:
            kwPayloads.append(doc.get("_source", {}).get("kwPayloads", ""))

        return kwPayloads

    def updateImageKwPayloads(self, batches=[], indexName=None):
        """

        :param batches: [('imageId','kwPayloads'),]
        :return:
        """
        imageIds = []
        for image in batches:
            imageIds.append(image[0])

        oldKwPayloads = self.getKwPayloadsByImageIds(
            indexName=indexName, imageIds=imageIds
        )
        assert len(oldKwPayloads) == len(imageIds)
        results = []
        for image, oldKwPayloads in zip(batches, oldKwPayloads):
            imageId = image[0]
            newKwPayloads = image[1]
            # new keyword payload replace old
            # 狗|0.9 猫|0.4"
            oldKwPayloadMap = {}
            new_ = newKwPayloads.split(" ")
            old_ = oldKwPayloads.split(" ")
            for old__ in old_:
                if not old__ == "":
                    kw = old__.split("|")[0]
                    score = old__.split("|")[1]
                    oldKwPayloadMap[kw] = score

            for new__ in new_:
                if not new__ == "":
                    kw = new__.split("|")[0]
                    score = new__.split("|")[1]
                    oldKwPayloadMap[kw] = score

            updatedKwPayloads_ = []
            for kw, score in oldKwPayloadMap.items():
                updatedKwPayloads_.append("%s|%s" % (kw, str(score)))

            updatedKwPayloads = " ".join(updatedKwPayloads_)
            logger1.debug(
                "update imageId %s KwPayloads from oldKwPayloads %s to updatedKwPayloads %s"
                % (imageId, oldKwPayloads, updatedKwPayloads)
            )
            result = self.updateByQuery(
                indexName=indexName,
                updatedField="kwPayloads",
                updatedValue=updatedKwPayloads,
                queryField="imageId",
                queryValue=imageId,
            )
            results.append(result)
        return results

    def queryImagesByKwIds(self, kwIds=None, lastScore=None, lastImageId=None):
        assert kwIds != None and len(kwIds) > 0
        if lastScore is None:
            logger1.info("first page image query by kwIds:{}", kwIds)
        search_after = None
        if lastScore is not None:
            assert lastImageId is not None
            search_after = [0, lastImageId]

    def pgQueryImagesByKwIds(self, indexName=None, kwIds=None, pageNum=1, pageSize=50):
        assert kwIds != None and len(kwIds) > 0
        fromIndex = (pageNum - 1) * pageSize
        shouldQuerys = []
        for kwId in kwIds:
            shouldQuerys.append({"payload_term": {"kwPayloads": kwId}})
        query = {
            "from": fromIndex,
            "size": pageSize,
            "query": {"bool": {"should": shouldQuerys, "minimum_should_match": 1}},
        }
        logger1.debug(query)
        result = self.client.search(body=query, index=indexName)

        docs = []
        matchedDocs = result.get("hits", {}).get("hits", [])
        if len(matchedDocs) == 0:
            docs.append({})
        else:
            for doc in matchedDocs:
                docs.append(doc)
        return docs
