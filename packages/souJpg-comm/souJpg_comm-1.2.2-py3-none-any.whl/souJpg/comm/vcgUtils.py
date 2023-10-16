from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import sys
import uuid
import hashlib


import os.path
import random
import re
from operator import add
import csv
import numpy as np
import math

import cv2

import mysql.connector
import requests


def ivecs_read(fname):
    a = np.fromfile(fname, dtype="int32")
    d = a[0]
    return a.reshape(-1, d + 1)[:, 1:].copy()


def fvecs_read(fname):
    return ivecs_read(fname).view("float32")


def ivecs_mmap(fname):
    a = np.memmap(fname, dtype="int32", mode="r")
    d = a[0]
    return a.reshape(-1, d + 1)[:, 1:]


def fvecs_mmap(fname):
    return ivecs_mmap(fname).view("float32")


def bvecs_mmap(fname):
    x = np.memmap(fname, dtype="uint8", mode="r")
    d = x[:4].view("int32")[0]
    return x.reshape(-1, d + 4)[:, 4:]


def ivecs_write(fname, m):
    n, d = m.shape
    m1 = np.empty((n, d + 1), dtype="int32")
    m1[:, 0] = d
    m1[:, 1:] = m
    m1.tofile(fname)


def fvecs_write(fname, m):
    m = m.astype("float32")
    ivecs_write(fname, m.view("int32"))


# used to get imageUrl from vcg mysql database based on imageIds
def getVcgImageUrl(imageId=None, mycursor=None):

    imageDomain = "http://bj-feiyuantu.oss-cn-beijing.aliyuncs.com/"

    mycursor.execute("SELECT oss_400,id FROM res_image where id='" + imageId + "'")
    myresult = mycursor.fetchall()

    imageUrl = imageDomain + myresult[0][0]

    return imageUrl


# mysqlUrl = "jdbc:mysql://rm-2zec526nd9v7a99n3.mysql.rds.aliyuncs.com:3306/resource23"
# mysqlUserName = "bi"
# mysqlPasswd = "bi@123abc"
# dbs={}
#
# mydb = mysql.connector.connect(
#         host="rm-2zec526nd9v7a99n3.mysql.rds.aliyuncs.com",
#         user=mysqlUserName,
#         passwd=mysqlPasswd,
#         database="resource23"
#     )


def getVcgImageUrl1(imageId=None, mycursor=None):

    mycursor.execute("SELECT oss_400,id FROM res_image where id='" + imageId + "'")
    myresult = mycursor.fetchall()
    imageDomain = "http://bj-feiyuantu.oss-cn-beijing.aliyuncs.com/"

    imageUrl = imageDomain + myresult[0][0]

    return imageUrl


# def getVcgImageUrls(imageIds=[],mydb=None):
#
#     mycursor = mydb.cursor()
#     sql="SELECT oss_400,id FROM res_image where id in (" + ','.join(imageIds) + ") "
#     print(sql)
#
#     mycursor.execute(sql)
#     myresult = mycursor.fetchall()
#
#     imageUrl=imageDomain+myresult[0][0]
#
#     mycursor.close()
#     mydb.close
#
#     return imageUrl


def getLowestScoreLabel(labelScoresCsvFile=None, keeplabelsNum=1000):
    labels = []
    boundry = keeplabelsNum
    num = 0
    with open(labelScoresCsvFile, "r") as f:
        for line in f.readlines():
            values = line.split(",")
            if num > boundry:
                labels.append(values[0])
            num += 1
    labels = [int(x) for x in labels]

    return labels


def getTuplesFromCsv(csvFile=None, seperator="\t"):
    tuples = []
    with open(csvFile, "r") as f:
        for line in f.readlines():
            tuple = line.split(seperator)
            tuple_ = []
            for tup in tuple:
                tuple_.append(tup.replace("\n", ""))

            tuples.append(tuple_)
    return tuples


def getKwsIndex(kwsIndexFile=None, seperator="\t"):
    kwsIndexMap = {}
    with open(kwsIndexFile, "r") as f:
        for line in f.readlines():
            class_id = line.split(seperator)[0].replace("\n", "")
            class_name = line.split(seperator)[1].replace("\n", "")
            kwsIndexMap[str(int(class_id))] = class_name
    return kwsIndexMap


def getIndexDetailsMap(indexMappingFile=None, detailsMappingFile=None, seperator="\t"):
    """

    :param indexMappingFile:  labedId \t identity
    :param detailsmappingFile: identity \t details
    :return:  finalMap,kwsIndexMap  , 如果detailsMappingFile None， finalMap 为 {} className=detailName
    """

    kwsIndexMap = {}
    kwsDetailMap = {}
    finalMap = {}

    with open(indexMappingFile, "r") as f:
        for line in f.readlines():
            class_id = line.split(seperator)[0].replace("\n", "")
            class_name = line.split(seperator)[1].replace("\n", "")
            kwsIndexMap[str(int(float(class_id)))] = class_name
    if detailsMappingFile is not None:
        with open(detailsMappingFile, "r") as f:
            for line in f.readlines():
                if len(line.split(seperator)) < 2:
                    continue
                class_id = line.split(seperator)[0].replace("\n", "")
                class_name = line.split(seperator)[1].replace("\n", "")
                kwsDetailMap[class_id] = class_name
        for key, value in kwsIndexMap.items():
            finalMap[key] = kwsDetailMap.get(value)

    return finalMap, kwsIndexMap


import traceback


def get_log_traceback(ex):

    ex_traceback = ex.__traceback__
    tb_lines = [
        line.rstrip("\n")
        for line in traceback.format_exception(ex.__class__, ex, ex_traceback)
    ]
    return tb_lines


def create_class_weight(labels_dict, mu=0.1, scaleFactor=4):
    total = np.sum(list(labels_dict.values()))
    classNum = len(labels_dict.keys())
    keys = labels_dict.keys()
    class_weight = np.zeros((classNum,), dtype=float)

    for key in keys:
        score = pow(mu * math.log(total / float(labels_dict.get(key))), scaleFactor)
        class_weight[key] = score  # if score > 1.0 else 1.0

    return class_weight


def create_class_weight1(
    labels_dict, scaleFactor=4, excludeLabels=[], labelAverageNum=None
):
    total = np.sum(list(labels_dict.values()))
    print(total)
    if labelAverageNum is None:
        labelAverageNum = total / (len(labels_dict.keys()) - len(excludeLabels))

    print(labelAverageNum)

    classNum = len(labels_dict.keys())
    keys = labels_dict.keys()
    class_weight = np.zeros((classNum,), dtype=float)

    for key in keys:
        if key in excludeLabels:
            continue
        score = labelAverageNum / labels_dict.get(key)
        class_weight[key] = score  # if score > 1.0 else 1.0

    return class_weight


def create_class_weight2(labels_dict, scaleFactor=4, excludeLabels=None):
    total = np.sum(list(labels_dict.values()))
    classNum = len(labels_dict.keys())
    keys = labels_dict.keys()
    class_weight = np.zeros((classNum,), dtype=float)

    for key in keys:
        if key in excludeLabels:
            continue
        score = 1 - float(labels_dict.get(key)) / total
        class_weight[key] = score  # if score > 1.0 else 1.0

    return class_weight


def getClassWeightVector(
    class_count_file=None, scaleFactor=None, excludeLabels=[], labelAverageNum=None
):
    if class_count_file is None:
        return None
    class_weight = None
    dic = {}
    with open(class_count_file) as file:
        csvReader = csv.reader(file, delimiter="\t")
        for row in csvReader:
            lableIndex = int(row[0])
            if lableIndex in excludeLabels:
                labelCount = 0.0
            else:
                labelCount = float(row[2])

            dic[lableIndex] = labelCount
        print(dic)
    class_weight = create_class_weight1(
        dic,
        scaleFactor=scaleFactor,
        excludeLabels=excludeLabels,
        labelAverageNum=labelAverageNum,
    )

    return class_weight


def getUuid():
    uuidStr = str(uuid.uuid1())
    return uuidStr


def computeMD5hash(my_string):
    m = hashlib.md5()
    m.update(my_string.encode("utf-8"))
    return m.hexdigest()


def printExceptionMessage(message=None, e=None):
    print("%s:%s" % (message, str(e)))
    print("-" * 60)
    traceback.print_exc(file=sys.stdout)
    print("-" * 60)


def getLastPartOfUri(uri=None):
    """

    :param uri: like: 'hdfs://gpu0.dev.yufei.com:9000/data/mlib_data/models/modelsConfig/vcgmla300_9_7.yml'
    :return:
    """

    str = uri.rsplit("/", 1)[-1]
    str = re.sub(r"\..*", "", str)
    return str
