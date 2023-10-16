import io
import os
import re
import sys
from io import BytesIO

import pyarrow as pa

import subprocess
from subprocess import PIPE
from loguru import logger as logger1

import traceback


class HdfsWraper(object):
    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port

        # traceback.print_stack()
        # print('i was executed!')
        try:
            self.hdfs = pa.hdfs.connect(host, port)
            # self.hdfs = fs.HadoopFileSystem(host, port )

        except BaseException as e:
            print("process  error:%s" % str(e))
            print("-" * 60)
            traceback.print_exc(file=sys.stdout)
            print("-" * 60)
            logger1.warning("can not connect hdfs!")

            self.hdfs = None

    def upload(self, tmpFilePath, hdfsFilePath, deleteLocal=True):
        """

        :param filePath:
        :return:
        upload file to remote hdfs cluster and delete the original file from tmp directory
        """

        with open(tmpFilePath, "rb") as fin:
            data = io.BytesIO(fin.read())
            self.hdfs.upload(hdfsFilePath, data)
            print("upload file:%s to hdfs: %s" % (tmpFilePath, hdfsFilePath))
        # delete tmpFilePath
        if deleteLocal:
            os.remove(tmpFilePath)
            print("delete local file:%s " % tmpFilePath)

    def uploadBigFile(self, tmpFilePath, hdfsFilePath, deleteLocal=True):

        cmd = "hadoop fs -copyFromLocal -f %s %s" % (tmpFilePath, hdfsFilePath)
        print("execute cmd: %s" % cmd)

        result = subprocess.run(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        exit_code = result.returncode
        stdout = result.stdout
        stderr = result.stderr
        print("stdout:%s" % stdout)
        print("stderr:%s" % stderr)

        if exit_code != 0:
            raise Exception("upload big file not succeed!")
        if deleteLocal:
            os.remove(tmpFilePath)
            print("delete local file:%s " % tmpFilePath)

    def downloadBigFile(self, hdfsFilePath, tmpFilePath):

        cmd = "hadoop fs -copyToLocal -f %s %s" % (hdfsFilePath, tmpFilePath)
        print("execute cmd: %s" % cmd)

        result = subprocess.run(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        exit_code = result.returncode
        stdout = result.stdout
        stderr = result.stderr
        print("stdout:%s" % stdout)
        print("stderr:%s" % stderr)
        if exit_code != 0:
            raise Exception("download  big file not succeed!")

    def download(self, hdfsFilePath, tmpFilePath):
        """

        :param hdfsFilePath:
        :param tmpFilePath:
        :return:

        """
        out_buf = BytesIO()
        self.hdfs.download(hdfsFilePath, out_buf)
        out_buf.seek(0)
        with open(tmpFilePath, "wb") as out:  ## Open temporary file as bytes
            out.write(out_buf.read())
        print("download hdfs file:%s to %s" % (hdfsFilePath, tmpFilePath))

    def ls(self, hdfsPath=None, pattern=None, hdfsPrefix=True):

        fileList = self.hdfs.ls(hdfsPath)
        fileList_ = []
        if pattern is not None:
            for fileName in fileList:
                # print(fileName)
                fileName1 = fileName.split("/")[-1]
                r = re.match(pattern, fileName1)
                if r:
                    fileName = "hdfs://%s:%d%s" % (self.host, self.port, fileName)
                    fileList_.append(fileName)
            fileList = fileList_

        return fileList

    def downloadFoler(self, hdfsPath=None, tmpFolder=None, pattern=None):
        fileList = self.hdfs.ls(hdfsPath)
        for filePath in fileList:
            fileName = filePath.split("/")[-1]
            fileHdfsPath = "hdfs://%s:%d%s" % (self.host, self.port, filePath)
            localFilePath = tmpFolder + fileName
            self.download(hdfsFilePath=fileHdfsPath, tmpFilePath=localFilePath)
            print(
                "download fileHdfsPath: %s to localFilePath %s "
                % (fileHdfsPath, localFilePath)
            )

    def createFolder(self, hdfsFilePath=None):
        self.hdfs.mkdir(hdfsFilePath)

    def checkFileExist(self, hdfsFilePath=None):

        return self.hdfs.exists(path=hdfsFilePath)

    def close(self):
        if self.hdfs is not None:
            self.hdfs.close()

    @staticmethod
    def createHdfsClient():
        hdfsWraper = None
        try:
            host = "gpu0.dev.yufei.com"

            port = 9000
            hdfsWraper = HdfsWraper(host=host, port=port)

        except Exception as e:
            print("error to init hdfs")
            print(str(e))
        return hdfsWraper
