from __future__ import absolute_import, division, print_function

import json
import time
from typing import List

import shortuuid
from loguru import logger as logger1

# from elasticsearch import Elasticsearch, helpers
from opensearchpy import OpenSearch, helpers

from souJpg import gcf
from souJpg.comm.contextManagers import ExceptionCatcher
from souJpg.comm.utils import singleton


@singleton
class EsBasedOps:
    def __init__(self, params={}):
        self.params = params
        esHosts =  gcf.esHosts
        if isinstance(esHosts, str):
            esHosts=esHosts.split(",")
       
           
        esHosts = self.params.get("esHosts",esHosts)
        logger1.debug(esHosts)
            
            

        self.esClient = OpenSearch(
            esHosts,
            sniff_on_start=gcf.sniff_on_start,
            sniff_on_connection_fail=gcf.sniff_on_connection_fail,
            sniffer_timeout=gcf.sniffer_timeout,
            max_retries=gcf.max_retries,
            
            retry_on_timeout=gcf.retry_on_timeout,
        )

    def getAllIndexNames(self):
        indexNames = [x for x in self.esClient.indices.get_alias("*").keys()]
        return indexNames

    def buildIndex(self, indexName=None, settings=None):
        if self.esClient.indices.exists(indexName):
            self.esClient.indices.delete(index=indexName)
        self.esClient.indices.create(index=indexName, body=settings)

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
        result = self.esClient.update_by_query(
            index=indexName,
            body=updatedBody,
            params={
                "conflicts": "proceed",
            },
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
        result = helpers.bulk(
            self.esClient, actions, stats_only=True, raise_on_error=True
        )
        logger1.info(result)

        return result

    def deleteImage(self, indexName=None, source=None, imageId=None):
        """
        delete image by imageId
        :return:
        """

        imageId = shortuuid.uuid(name="%s_%s" % (source, imageId))
        self.esClient.delete(index=indexName, id=imageId)

    def batchDelete(self, actions=[]):
        """
        action = {'_op_type': 'delete', '_index': indexName, '_type': '_doc', '_id': id}
        :return:
        """
        result = helpers.bulk(
            self.esClient, actions, stats_only=True, raise_on_error=True
        )
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
        result = self.esClient.search(body=query, index=indexName)
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

        result = self.esClient.msearch(index=indexName, body=request)
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

    def queryByIds(self, ids=None, indexName=None):
        search_arr = []
        sources = []

        for _id in ids:
            # req_head
            search_arr.append({"index": indexName})
            # req_body
            search_arr.append(
                {
                    "query": {"match": {"_id": _id}},
                    "from": 0,
                    "size": 1,
                }
            )
        request = ""
        for each in search_arr:
            request += "%s \n" % json.dumps(each)

        result = self.esClient.msearch(index=indexName, body=request)
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
            doc = doc.get("_source", {})
            sources.append(doc)
        return sources

    def getImageConcepts(self, sources=None, imageIds=None, indexName=None):
        search_arr = []
        conceptses = []

        for source, imageId in zip(sources, imageIds):
            _id = shortuuid.uuid(name="%s_%s" % (source, imageId))
            # req_head
            search_arr.append({"index": indexName})
            # req_body
            search_arr.append(
                {
                    "query": {"match": {"_id": _id}},
                    "from": 0,
                    "size": 1,
                }
            )
        request = ""
        for each in search_arr:
            request += "%s \n" % json.dumps(each)

        result = self.esClient.msearch(index=indexName, body=request)
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
            concepts = doc.get("_source", {}).get("concepts", [])

            conceptses.append(concepts)
        logger1.debug(
            "sources:{},imageIds:{},conceptses:{}", sources, imageIds, conceptses
        )
        return conceptses

    def updateImageConcepts(
        self, sources=None, imageIds=None, newConcept=None, indexName=None
    ):
        conceptses = self.getImageConcepts(
            sources=sources, imageIds=imageIds, indexName=indexName
        )
        docs = []
        for source, imageId, concepts in zip(sources, imageIds, conceptses):
            doc = {}
            _id = shortuuid.uuid(name="%s_%s" % (source, imageId))

            doc["_id"] = _id
            updatedConcepts = set(concepts)
            updatedConcepts.add(newConcept)
            doc["concepts"] = list(updatedConcepts)
            docs.append(doc)
        self.batchUpdate(indexName=indexName, op_type="update", docs=docs)

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
        result = self.esClient.search(body=query, index=indexName)

        docs = []
        matchedDocs = result.get("hits", {}).get("hits", [])
        if len(matchedDocs) == 0:
            docs.append({})
        else:
            for doc in matchedDocs:
                docs.append(doc)
        return docs

    def opqQuery(self, params={}):
        """

        :param indexName:
        :param opq_features:
        :param vectorReRank:
        :param topNum:  最后返回的topNum documents， 如果vectorReRank开启的话，则是topNum*shardNum,后续想办法解决
        :return:
        """
        logger1.info("EsClient->opqQuery params: {}", params)
        enLargeFactor = params["enLargeFactor"]
        indexName = params["indexName"]
        opq_features = params["opq_features"]
        vectorReRank = params["vectorReRank"]
        topNum = params["topNum"]
        opqKey = params["opqKey"]
        routingValues = params["routingValues"]

        req_head = {"index": indexName}

        request = []
        tic = time.perf_counter()
        if vectorReRank:
            for opq_feature, routingValue in zip(opq_features, routingValues):
                req_body = {
                    "query": {"match": {"opq_features": opq_feature}},
                    "rescore": {
                        "vectors_rerank": {
                            "vectorFieldName": "opq_features",
                            "inputCodes": opq_feature,
                            "opqKey": opqKey,
                        },
                        "window_size": topNum,
                    },
                    "from": 0,
                    "size": topNum * enLargeFactor,
                }
                req_head_ = req_head.copy()
                if routingValue is not None:
                    req_head_["routing"] = routingValue

                request.extend([req_head_, req_body])

        else:
            for opq_feature, routingValue in zip(opq_features, routingValues):
                req_body = {
                    "query": {"match": {"opq_features": opq_feature}},
                    "from": 0,
                    "size": topNum,
                }
                req_head_ = req_head.copy()
                if routingValue is not None:
                    req_head_["routing"] = routingValue

                request.extend([req_head_, req_body])
        logger1.trace("EsClient->opqQuery: {}", request)
        resp = self.esClient.msearch(body=request, request_timeout=100)

        toc = time.perf_counter()
        logger1.debug(
            "EsClient->opqQuery vectorReRank is {}, and spent time: {} ms ",
            vectorReRank,
            1000 * (toc - tic),
        )
        logger1.trace("batch query resp : {}", resp)
        return resp

    def keywordsSuggest(self, indexName, suggestQuery=None):
        suggestedKeywords = []

        logger1.debug("keywords suggest query: {}", suggestQuery)
        result = self.esClient.search(body=suggestQuery, index=indexName)

        docs = []

        matchedDocs = (
            result.get("suggest", {}).get("suggested", [])[0].get("options", [])
        )
        logger1.debug(matchedDocs)
        return matchedDocs
