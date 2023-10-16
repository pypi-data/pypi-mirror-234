from __future__ import absolute_import, division, print_function

import abc
import csv
import os.path
import random
import re
import zipfile
from operator import add

import cv2
import mysql.connector
import pyspark
import pyspark.sql.functions as f
import requests
from pyspark.ml.feature import StringIndexer
from pyspark.mllib.evaluation import MultilabelMetrics
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.types import Row, StringType, StructField, StructType
from pyspark.sql.window import Window
from pyspark.storagelevel import StorageLevel

from souJpg.comm import hdfsUtils, vcgUtils


class SparkBase(abc.ABC):
    def __init__(self):
        host = "gpu0.dev.yufei.com"
        port = 9000
        self.hdfsWraper = hdfsUtils.HdfsWraper(host=host, port=port)

    def createSparkEnv(self):
        # spark.pyspark.python
        conf = pyspark.SparkConf()

        conf.set("spark.executor.memory", "10g")

        spark = (
            SparkSession.builder.appName("myApp")
            .master("spark://gpu0.dev.yufei.com:7077")
            .config(conf=conf)
            .getOrCreate()
        )
        """
        .conf("spark.mongodb.input.uri", "mongodb://zhaoyufei:vcgjasstion@gpu0.dev.yufei.com/vcg.evaluations")\
        .conf("spark.mongodb.output.uri",
                    "mongodb://zhaoyufei:vcgjasstion@gpu0.dev.yufei.com/vcg.evaluations_result")\
         .conf('spark.mongodb.input.partitioner','MongoPaginateByCountPartitioner') \
            .conf('spark.mongodb.input.partitionerOptions.numberOfPartitions',128) \
        """

        return spark

    def createYarnSparkEnv(self):
        projectPath = "/data/projects/imageAI/"
        hdfsPath = "hdfs://gpu0.dev.yufei.com:9000/data/zhaoyufei/imageAI.zip"
        # print('start to package imageAI and upload to hdfs...')
        # self.updateVcgImageAI(vcgImageAIPath=projectPath,hdfsPath=hdfsPath)

        # spark.pyspark.python
        conf = pyspark.SparkConf()
        # conf.set('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.3.1')
        # ,/data/software/mongo-spark-connector_2.11-2.3.1.jar
        # conf.set('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.4.1')

        # conf.set('spark.yarn.jars',
        #          "/data/software/spark_lib/spark-tensorflow-connector_2.12-1.10.0.jar,/data/software/spark_lib/mongo-java-driver-3.8.2.jar,/data/software/spark_lib/mongo-spark-connector_2.12-2.4.1.jar")
        conf.set("spark.driver.maxResultSize", "20g")
        conf.set("spark.driver.memory", "3g")
        #'spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.3.2'
        # conf.set('spark.executor.memory', '5g')
        # conf.set('spark.executor.instances',10)
        # conf.set('spark.executorEnv.PYSPARK_PYTHON','/data/miniconda3/envs/imageAI/bin/python')
        # conf.set('spark.yarn.appMasterEnv.PYSPARK_PYTHON','/data/miniconda3/envs/imageAI/bin/python')

        spark = (
            SparkSession.builder.appName("myApp")
            .master("yarn")
            .config(conf=conf)
            .getOrCreate()
        )
        """
        .conf("spark.mongodb.input.uri", "mongodb://zhaoyufei:vcgjasstion@gpu0.dev.yufei.com/vcg.evaluations")\
        .conf("spark.mongodb.output.uri",
                    "mongodb://zhaoyufei:vcgjasstion@gpu0.dev.yufei.com/vcg.evaluations_result")\
         .conf('spark.mongodb.input.partitioner','MongoPaginateByCountPartitioner') \
            .conf('spark.mongodb.input.partitionerOptions.numberOfPartitions',128) \
        """

        return spark

    def createLocalSparkEnv(self):
        # spark.pyspark.python
        conf = pyspark.SparkConf()
        # conf.set('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.3.1')
        # ,/data/software/mongo-spark-connector_2.11-2.3.1.jar
        # conf.set('spark.jars',
        #          "/data/software/spark_lib/spark-tensorflow-connector_2.11-1.11.0-rc2.jar,/data/software/spark_lib/mongo-spark-connector_2.11-2.3.1.jar,/data/software/spark_lib/mongo-java-driver-3.8.2.jar")
        # conf.set('spark.executor.memory', '3g')

        spark = SparkSession.builder.appName("myApp").config(conf=conf).getOrCreate()
        # .master("spark://gpu0.dev.yufei.com:7077") \
        # .conf("spark.mongodb.input.uri", "mongodb://zhaoyufei:vcgjasstion@gpu0.dev.yufei.com/vcg.evaluations") \
        # .conf("spark.mongodb.output.uri",
        #         "mongodb://zhaoyufei:vcgjasstion@gpu0.dev.yufei.com/vcg.evaluations_result") \

        return spark
