from __future__ import absolute_import, division, print_function

import abc
import csv
import os.path
import random
import re
import subprocess
import zipfile
from operator import add
from subprocess import PIPE

import cv2
import mysql.connector
import pyspark
import pyspark.sql.functions as f
import requests
import yaml
from pyspark.ml.feature import StringIndexer
from pyspark.mllib.evaluation import MultilabelMetrics
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.types import Row, StringType, StructField, StructType
from pyspark.sql.window import Window
from pyspark.storagelevel import StorageLevel

from souJpg.comm import vcgUtils


class SparkApp:
    def __init__(self, configFile=None):
        with open(configFile, "r", encoding="utf-8") as ymlfile:
            config = yaml.load(ymlfile)
        # spark-submit related config:
        self.config = config
        self.appName = self.config.get("appName")
        self.cmd = self.buildCmd()

    def buildCmd(self):
        cmd = (
            "nohup spark-submit --master yarn   --py-files {py_files}   --archives {archives}  "
            "--deploy-mode cluster --name {appName} --num-executors {num_executors} --executor-cores {executor_cores} --executor-memory {executor_memory} "
            "--conf spark.yarn.executor.nodeLabelExpression={executor_nodeLabelExpression} --conf spark.yarn.am.nodeLabelExpression={am_nodeLabelExpression} "
            "--conf spark.yarn.appMasterEnv.PYSPARK_PYTHON={PYSPARK_PYTHON}     --queue {queue} {appPyFileName}  "
        )

        appName = self.config.get("appName")
        py_files = self.config.get("py_files")
        archives = self.config.get("archives")
        num_executors = self.config.get("num_executors")
        executor_cores = self.config.get("executor_cores")
        executor_memory = self.config.get("executor_memory")
        executor_nodeLabelExpression = self.config.get("executor_nodeLabelExpression")
        am_nodeLabelExpression = self.config.get("am_nodeLabelExpression")
        PYSPARK_PYTHON = self.config.get("PYSPARK_PYTHON")
        queue = self.config.get("queue")
        appPyFileName = self.config.get("appPyFileName")
        cmd = cmd.format(
            appName=appName,
            py_files=py_files,
            archives=archives,
            num_executors=num_executors,
            executor_cores=executor_cores,
            executor_memory=executor_memory,
            executor_nodeLabelExpression=executor_nodeLabelExpression,
            am_nodeLabelExpression=am_nodeLabelExpression,
            PYSPARK_PYTHON=PYSPARK_PYTHON,
            queue=queue,
            appPyFileName=appPyFileName,
        )

        cmd.format()
        return cmd

    def run(self, appArgs={}):
        cmd = self.cmd
        appArgsStr = ""
        for key, value in appArgs.items():
            appArgsStr += "--" + key + " " + str(value) + " "
        cmd += appArgsStr + " > /dev/null &"

        print("execute cmd: %s" % cmd)

        result = subprocess.run(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        exit_code = result.returncode
        stdout = result.stdout.decode("utf-8")
        stderr = result.stderr.decode("utf-8")
        for line in str(stdout).split("\n"):
            print(line)
        for line in stderr.split("\n"):
            print(line)

        if exit_code != 0:
            raise Exception("execute sparkApp error!")
        else:
            print("end to execute sparkApp!")
