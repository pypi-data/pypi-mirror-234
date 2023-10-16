from __future__ import absolute_import, division, print_function

import csv
import sys
import traceback

from loguru import logger as logger1

from souJpg.comm import hdfsUtils, vcgUtils

# from pymongo import InsertOne, UpdateOne
# from pymongo import MongoClient
# uri = "mongodb://zhaoyufei:vcgjasstion@gpu0.dev.yufei.com:27017/vcg?authMechanism=SCRAM-SHA-1"
# client = MongoClient(uri)
"""
从mongodb 中获取某个模型的labels相关信息 ， 比如：per label count to compute class weights, labelsName mapping...
"""


def loadLabelsInfo(labelsType=None):
    return None


"""
解析各种格式的labelIndex 信息然后存入mongodb labels表中
"""


def parseAndSaveLabels(labelsIndexFile=None, **kwargs):
    return None


class LabelUtils:
    @staticmethod
    def createIndexAndDetailMappingFile(csvFile=None, seperator="\t", savedFolder=None):
        # index,className, detailName    ,隔开
        indexMappingFile = "%s%s" % (savedFolder, "labelsIndexMapping.csv")
        detailsMappingFile = "%s%s" % (savedFolder, "labelsDetailsMapping.csv")
        indexDetailsMappingFile = "%s%s" % (savedFolder, "indexDetailsMapping.csv")

        indexMappingList = []
        detailsMappingList = []
        indexDetailsMapping = []

        with open(csvFile, "r", encoding="utf-8") as f:
            for line in f.readlines():
                values = line.split(seperator)
                assert len(values) >= 2
                index = values[0].replace("\n", "")
                className = None
                detailName = None
                if len(values) == 2:
                    className = values[1].replace("\n", "")
                    detailName = className
                if len(values) > 2:
                    className = values[1].replace("\n", "")
                    detailName = values[2].replace("\n", "")
                indexMappingList.append([index, className])
                detailsMappingList.append([className, detailName])
                indexDetailsMapping.append([index, detailName])
        with open(indexMappingFile, "w", newline="\n", encoding="utf-8") as csvfile:
            filewriter = csv.writer(
                csvfile, delimiter="\t", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            for indexMapping in indexMappingList:
                filewriter.writerow(indexMapping)
        with open(detailsMappingFile, "w", newline="\n", encoding="utf-8") as csvfile:
            filewriter = csv.writer(
                csvfile, delimiter="\t", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            for detailsMapping in detailsMappingList:
                filewriter.writerow(detailsMapping)
        with open(
            indexDetailsMappingFile, "w", newline="\n", encoding="utf-8"
        ) as csvfile:
            filewriter = csv.writer(
                csvfile, delimiter="\t", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            for detailsMapping in indexDetailsMapping:
                filewriter.writerow(detailsMapping)

    def __init__(self, config=None):
        seperator = "\t"
        # print(type(HdfsWraper))

        hdfsWraper = hdfsUtils.HdfsWraper.createHdfsClient()

        if isinstance(config, dict):
            indexMappingFile = config.get("indexMappingFile")
            detailsMappingFile = config.get("detailsMappingFile")
        else:
            # VcgCfg
            indexMappingFile = config.indexMappingFile
            detailsMappingFile = config.detailsMappingFile

        if indexMappingFile is not None:
            if indexMappingFile.startswith("hdfs://"):
                try:
                    tmpPath = "/tmp/" + vcgUtils.getUuid()
                    hdfsWraper.download(
                        hdfsFilePath=indexMappingFile, tmpFilePath=tmpPath
                    )
                    indexMappingFile = tmpPath
                except BaseException as e:
                    # print(str(e))
                    # print("-" * 60)
                    # traceback.print_exc(file=sys.stdout)
                    # print("-" * 60)
                    logger1.warning(
                        "can not download indexMappingFile, maybe hdfs connect error "
                    )

        if detailsMappingFile is not None:
            if detailsMappingFile.startswith("hdfs://"):
                try:
                    tmpPath = "/tmp/" + vcgUtils.getUuid()
                    hdfsWraper.download(
                        hdfsFilePath=detailsMappingFile, tmpFilePath=tmpPath
                    )
                    detailsMappingFile = tmpPath

                except BaseException as e:
                    logger1.warning(
                        "can not download detailsMappingFile, maybe hdfs connect error, or detailsMappingFile not existed"
                    )

        if hdfsWraper is not None:
            hdfsWraper.close()

        # index to className
        self.kwsIndexMap = {}
        # className to detail
        self.kwsDetailMap = {}
        # index to detail
        self.finalMap = {}
        self.reverseKwsIndexMap = {}
        self.kwsDetail2IndexMap = {}

        self.kwsSet = set()
        try:
            if indexMappingFile:
                with open(indexMappingFile, "r", encoding="utf-8") as f:
                    for line in f.readlines():
                        class_id = line.split(seperator)[0].replace("\n", "")
                        class_name = line.split(seperator)[1].replace("\n", "")
                        self.kwsIndexMap[str(int(float(class_id)))] = class_name
                        self.kwsSet.add(class_name)

            if detailsMappingFile:
                with open(detailsMappingFile, "r", encoding="utf-8") as f:
                    for line in f.readlines():
                        if len(line.split(seperator)) < 2:
                            continue
                        class_id = line.split(seperator)[0].replace("\n", "")
                        class_name = line.split(seperator)[1].replace("\n", "")
                        self.kwsDetailMap[class_id] = class_name

            for key, value in self.kwsIndexMap.items():
                self.finalMap[key] = self.kwsDetailMap.get(value)
            for key, value in self.finalMap.items():
                self.kwsDetail2IndexMap[value] = key

            for key, value in self.kwsIndexMap.items():
                self.reverseKwsIndexMap[value] = key
            for key, value in self.kwsIndexMap.items():
                self.reverseKwsIndexMap[value] = key

        except BaseException as e:
            print(str(e))
            print("-" * 60)
            traceback.print_exc(file=sys.stdout)
            print("-" * 60)

    def getDetailByIndex(self, index=None):
        return self.finalMap.get(index)

    def getDetailByClassName(self, className=None):
        return self.finalMap.get(self.reverseKwsIndexMap.get(className))

    def getClassNameByIndex(self, index=None):
        return self.kwsIndexMap.get(index)

    def getIndexByClassName(self, className=None):
        return self.reverseKwsIndexMap.get(className)

    def ifKwExist(self, className=None):
        return className in self.kwsSet


import pymongo
from bson.binary import Binary as BsonBinary
from pymongo import InsertOne, MongoClient, UpdateMany, UpdateOne


class MongoLabelUtils:
    def generatedIndexMappingFile(self, savedFolder=None, delimiter="\t"):
        indexMappingFile = "%s%s" % (savedFolder, "labelsIndexMapping.csv")
        detailsMappingFile = "%s%s" % (savedFolder, "labelsDetailsMapping.csv")
        indexDetailsMappingFile = "%s%s" % (savedFolder, "indexDetailsMapping.csv")

        with open(detailsMappingFile, "w", newline="\n", encoding="utf-8") as csvfile:
            filewriter = csv.writer(
                csvfile, delimiter=delimiter, quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            for kwId, detailName in self.kwsDetailMap.items():
                filewriter.writerow([kwId, detailName])
        with open(indexMappingFile, "w", newline="\n", encoding="utf-8") as csvfile:
            filewriter = csv.writer(
                csvfile, delimiter=delimiter, quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            for index, kwId in self.kwsIndexMap.items():
                filewriter.writerow([index, kwId])
        with open(
            indexDetailsMappingFile, "w", newline="\n", encoding="utf-8"
        ) as csvfile:
            filewriter = csv.writer(
                csvfile, delimiter=delimiter, quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            for index, kwId in self.finalMap.items():
                filewriter.writerow([index, kwId])

    def __init__(self, params={}):
        self.labelsQuery = params.get("labelsQuery", None)
        assert self.labelsQuery is not None
        mongoUri = "mongodb://zhaoyufei:vcgjasstion@gpu0.dev.yufei.com:27017/vcg?authSource=vcg"

        client = MongoClient(mongoUri)
        self.labelsTable = client["vcg"]["labels"]
        """
        labelId-> className, labelName->detailName, index sort by labelId-> index
        
        """
        # index to className
        self.kwsIndexMap = {}
        # className to detail
        self.kwsDetailMap = {}
        # index to detail
        self.finalMap = {}
        self.reverseKwsIndexMap = {}
        # className set
        self.kwsSet = set()
        labelInfos = self.labelsTable.find(self.labelsQuery).sort(
            "labelId", pymongo.DESCENDING
        )
        self.kwId2KwInfoMap = {}

        self.vcgKwId2LabelName = {}
        self.gettyKwId2LabelName = {}
        for index, labelInfo in enumerate(labelInfos):
            labelId = labelInfo["labelId"]
            self.kwsIndexMap[str(index)] = labelId
            self.kwsDetailMap[labelId] = labelInfo["labelName"]
            self.finalMap[str(index)] = labelInfo["labelName"]

            self.vcgKwId2LabelName[labelInfo["vcgKwId"]] = labelInfo["labelName"]
            self.gettyKwId2LabelName[labelInfo["gettyKwId"]] = index
            self.kwId2KwInfoMap[str(index)] = labelInfo

        for key, value in self.kwsIndexMap.items():
            self.reverseKwsIndexMap[value] = key

    def getDetailByIndex(self, index=None):
        return self.finalMap.get(index)

    def getDetailByClassName(self, className=None):
        return self.finalMap.get(self.reverseKwsIndexMap.get(className))

    def getClassNameByIndex(self, index=None):
        return self.kwsIndexMap.get(index)

    def getIndexByClassName(self, className=None):
        return self.reverseKwsIndexMap.get(className)

    def ifKwExist(self, className=None):
        return className in self.kwsSet

    def getLabelNameByVcgKwId(self, vcgKwId=None):
        return self.vcgKwId2LabelName.get(vcgKwId)

    def getLabelIndexByGettyKwId(self, gettyKwId=None):
        return self.gettyKwId2LabelName.get(gettyKwId)
