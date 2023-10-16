import base64
import io
import json
import os
import shutil
import time
import unittest
from random import randrange
import uuid

# import happybase
from loguru import logger as logger1
from numpy import linalg as LA
from omegaconf import OmegaConf
from PIL import Image as pil_image

from souJpg.comm import imageUtils
from souJpg.comm.cfg.utils import initGcf
from souJpg.comm.cfg.vcgCfg import VcgCfg
from souJpg.comm.contextManagers import ExceptionCatcher, methodRetryWraper
from souJpg.comm.dbHelper import createMongoDBConnection
from souJpg.comm.fs.distributeFs import MinioFs, TecentCosFs
from souJpg.comm.kafkaOps import ConsumerParams, KafkaOps, Message
from souJpg.comm.labelUtils import MongoLabelUtils
from souJpg.comm.redisOps import RedisOps, cached
from souJpg.comm.videoUtils import VideoParsedResult, parseVideo


class MongoLabelUtilsTest(unittest.TestCase):
    def test_init(self):
        params = {}
        labelsQuery = {
            "globalIdentity": "labels_14081",
        }
        params["labelsQuery"] = labelsQuery
        labelUtils = MongoLabelUtils(params=params)
        logger1.info("labels count:{}", len(labelUtils.kwsIndexMap.keys()))
        labelName = labelUtils.getLabelNameByVcgKwId(vcgKwId="25619")

        assert labelName == "罗马莴苣"

        # test export to indexMapping file
        savedFolder = r"C:\data\projects\imageAI\souJpg.comm\test\conf/"
        labelUtils.generatedIndexMappingFile(savedFolder=savedFolder, delimiter=",")

        # 测试两次读取的index保持一致
        labelId = "9qnyfxwj3ikhEF6Gd8A6Jw"
        RightDetailName = "特"
        testIndex = labelUtils.getIndexByClassName(className=labelId)

        detailName = labelUtils.getDetailByIndex(testIndex)
        logger1.debug("detailName:{}", detailName)

        labelUtils1 = MongoLabelUtils(params=params)
        detailName1 = labelUtils1.getDetailByIndex(testIndex)
        logger1.debug("detailName1:{}", detailName1)

        self.assertEqual(detailName1, detailName)

        self.assertEqual(labelUtils.getClassNameByIndex(index=testIndex), labelId)
        self.assertEqual(labelUtils.getDetailByIndex(index=testIndex), RightDetailName)
        self.assertEqual(labelUtils.getIndexByClassName(className=labelId), testIndex)


class CfgTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cfgFile = "cfg/base.yml"

    def test_cfg(self):
        gcf = VcgCfg.fromYaml(cfgFile=self.cfgFile)
        logger1.info(gcf.items)

    def test_omegaConf(self):
        baseConf = OmegaConf.load(self.cfgFile)
        logger1.info(baseConf)
        # test merge
        conf1 = OmegaConf.load("cfg/cfg1.yml")
        mergedConf = OmegaConf.merge(baseConf, conf1)
        logger1.info(mergedConf)
        logger1.info(type(mergedConf))
        logger1.info(baseConf.imagesTableMap)
        logger1.info(baseConf.dbURIMapping)
        logger1.info(gcf.dbURIMapping.get("imagesCore"))

    def test_cfgUtils(self):
        gcfConf = initGcf(baseConf=self.cfgFile)
        logger1.info(gcfConf)

    def test_gcf(self):
        from pathlib import Path

        from souJpg.comm.cfg.utils import (
            envVariablesSupportedList,
            initErrorCodeMap,
            initGcf,
        )

        filePath = Path(__file__).parent

        def get_project_root() -> Path:
            return Path(__file__).parent.parent

        project_path = get_project_root()

        gcf = initGcf(baseConf=str(filePath) + "/cfg/baseConf.yaml")
        for envVariable in envVariablesSupportedList:
            logger1.info("{}: {}", envVariable, gcf.get(envVariable))

        # logger1.info("gcf:{}", gcf)


class ImageUtilsTest(unittest.TestCase):
    def test_resizeAndBytesImageFromPath(self):
        testImagePath = "testImages/test.jpg"
        imageBytes = imageUtils.resizeAndBytesImageFromPath(imagePath=testImagePath)
        img = pil_image.open(io.BytesIO(imageBytes))
        original_w, original_h = img.size
        maxSize = original_w
        if maxSize < original_h:
            maxSize = original_h
        logger1.info("original_w: {},original_h:{}", original_w, original_h)

        targetSize = randrange(maxSize, maxSize + 100)
        imageBytes = imageUtils.resizeAndBytesImageFromPath(
            imagePath=testImagePath, targetSize=targetSize, inverse=True
        )
        img = pil_image.open(io.BytesIO(imageBytes))
        w, h = img.size
        self.assertEqual(h, targetSize)
        targetSize = randrange(maxSize, maxSize + 100)
        # ifSmallerNoResize 为true的时候, targetSize大于maxSize，不会进行resize
        imageBytes = imageUtils.resizeAndBytesImageFromPath(
            imagePath=testImagePath,
            targetSize=targetSize,
            inverse=True,
            ifSmallerNoResize=True,
        )
        img = pil_image.open(io.BytesIO(imageBytes))
        w, h = img.size
        self.assertEqual(h, original_h)
        self.assertEqual(w, original_w)
        # ifSmallerNoResize 为true的时候, targetSize小于于maxSize，正常进行resize
        targetSize = randrange(maxSize - 100, maxSize)
        #
        imageBytes = imageUtils.resizeAndBytesImageFromPath(
            imagePath=testImagePath,
            targetSize=targetSize,
            inverse=True,
            ifSmallerNoResize=True,
        )
        img = pil_image.open(io.BytesIO(imageBytes))
        w, h = img.size

    def test_resizeAndBytesImageFromUrl(self):
        url = "http://gpu0.dev.yufei.com:8005/image/autotags_5m/GsEaG6UGuMnbBcrb6qYN9H/"

        imageBytes = imageUtils.resizeAndBytesImageFromUrl(imageUrl=url)
        testImagePath = "testImages/test.jpg"
        imageBytes1 = imageUtils.resizeAndBytesImageFromPath(imagePath=testImagePath)
        img = pil_image.open(io.BytesIO(imageBytes))
        original_w, original_h = img.size
        maxSize = original_w
        if maxSize < original_h:
            maxSize = original_h
        logger1.info("original_w: {},original_h:{}", original_w, original_h)

        targetSize = randrange(maxSize, maxSize + 100)
        imageBytes = imageUtils.resizeAndBytesImageFromUrl(
            imageUrl=url, targetSize=targetSize, inverse=True
        )
        img = pil_image.open(io.BytesIO(imageBytes))
        w, h = img.size
        self.assertEqual(h, targetSize)
        targetSize = randrange(maxSize, maxSize + 100)
        # ifSmallerNoResize 为true的时候, targetSize大于maxSize，不会进行resize
        imageBytes = imageUtils.resizeAndBytesImageFromUrl(
            imageUrl=url, targetSize=targetSize, inverse=True, ifSmallerNoResize=True
        )
        img = pil_image.open(io.BytesIO(imageBytes))
        w, h = img.size
        self.assertEqual(h, original_h)
        self.assertEqual(w, original_w)
        # ifSmallerNoResize 为true的时候, targetSize小于于maxSize，正常进行resize
        targetSize = randrange(maxSize - 100, maxSize)
        #
        imageBytes = imageUtils.resizeAndBytesImageFromUrl(
            imageUrl=url, targetSize=targetSize, inverse=True, ifSmallerNoResize=True
        )
        img = pil_image.open(io.BytesIO(imageBytes))
        w, h = img.size
        self.assertEqual(h, targetSize)
        # resizeAndBytesImageFromPath

    def test_imagesMaker(self):
        # large, preview,medium
        """
        webp 原图越大压缩效果越好，如果原图过小，压缩效果不明显
        一般大于1000*1000的图片，压缩效果明显

        """
        urls = [
            "http://gpu0.dev.yufei.com:8007/image/images_pxhere/1082313/",
            "http://gpu0.dev.yufei.com:8007/image/images_unsplash/BgScE96CgQM/",
            "http://gpu0.dev.yufei.com:8007/image/images_unsplash/1i8xRkE8gXo/",
            "http://gpu0.dev.yufei.com:8007/image/images_unsplash/zNGQFub3gwU/",
        ]
        for j, url in enumerate(urls):
            imageBytes = imageUtils.resizeAndBytesImageFromUrl(imageUrl=url)
            with pil_image.open(io.BytesIO(imageBytes)) as img:
                if img.mode != "RGB":
                    img = img.convert("RGB")

                logger1.info(img.size)

            resolution, previewBytes, mediumBytes, largeBytes = imageUtils.imagesMaker(
                imageBytes=imageBytes
            )
            logger1.info(resolution)
            for i, image in enumerate([previewBytes, mediumBytes, largeBytes]):
                with pil_image.open(io.BytesIO(image)) as img:
                    img.save("tmp/%s-%s.webp" % (str(j), str(i)), format="webp")
                    logger1.info(img.size)

    def test_createWatermark(self):
        testImagePath = "testImages/test1.jpg"
        watermarkImagePath = "testImages/tool_watermarker.png"
        imageBytes = imageUtils.resizeAndBytesImageFromPath(imagePath=testImagePath)
        watermarkImageBytes = imageUtils.resizeAndBytesImageFromPath(
            imagePath=watermarkImagePath
        )

        finalImageBytes = imageUtils.createWatermark(
            imageBytes=imageBytes, watermarkImageBytes=watermarkImageBytes
        )
        with pil_image.open(io.BytesIO(finalImageBytes)) as img:
            # if img.mode != "RGB":
            #     img = img.convert("RGB")
            logger1.info(img.size)
            img.save("testImages/diff2_watermark.jpg", format="JPEG", quality=85)

    def test_imageFormatConvert(self):
        quality = 80
        testImagePath = "testImages/diff2.jpg"
        imageBytes = imageUtils.resizeAndBytesImageFromPath(
            imagePath=testImagePath, format="WEBP"
        )
        with pil_image.open(io.BytesIO(imageBytes)) as img:
            # if img.mode != "RGB":
            #     img = img.convert("RGB")
            logger1.info(img.size)
            img.save("testImages/test1.webp", format="WEBP", quality=quality)
        imageBytes = imageUtils.resizeAndBytesImageFromPath(
            imagePath=testImagePath, format="JPEG"
        )
        with pil_image.open(io.BytesIO(imageBytes)) as img:
            # if img.mode != "RGB":
            #     img = img.convert("RGB")
            logger1.info(img.size)
            img.save("testImages/test1_1.jpg", format="JPEG", quality=quality)
        imageBytes = imageUtils.resizeAndBytesImageFromPath(
            imagePath=testImagePath, format="PNG"
        )
        with pil_image.open(io.BytesIO(imageBytes)) as img:
            # if img.mode != "RGB":
            #     img = img.convert("RGB")
            logger1.info(img.size)
            img.save("testImages/test1.png", format="PNG", quality=quality)


class CommTest(unittest.TestCase):
    def test_createMongoDBConnection(self):
        db = createMongoDBConnection(dbType="imagesCoreDBURI")
        logger1.info(db)


from souJpg.comm.dbsCL import batchPut


class DbsClTest(unittest.TestCase):
    def setUp(self) -> None:
        host = "gpu0.dev.yufei.com"

        hbClient = happybase.Connection(host=host, port=9999, timeout=60000)
        self.imagesTable = hbClient.table("images")

    def test_accessHbase(self):
        imageId = "testImages/1.jpg".encode()
        image = self.imagesTable.row(imageId)
        if image is not None:
            logger1.info(image[b"c2:content"])

    def test_pushImagesToHbase(self):
        imagesFolder = "testImages/"
        _, _, testPaths = next(os.walk(imagesFolder))
        testPaths.extend(testPaths)

        logger1.debug(testPaths)
        puts = []
        inverse = True
        targetSize = 300
        for imagePath in testPaths:
            put = {}
            logger1.info(imagePath)
            imageBytes = None
            imageFullPath = imagesFolder + imagePath
            imageBytes = imageUtils.resizeAndBytesImageFromPath(
                imagePath=imageFullPath,
                targetSize=targetSize,
                inverse=inverse,
                ifSmallerNoResize=True,
            )
            img_b64encode = base64.b64encode(imageBytes)  # base64编码

            put = {"c0:imageId": imagePath, "c2:content": img_b64encode}
            puts.append(put)

        tableName = "images"
        params = {}
        params["puts"] = puts
        params["tableName"] = tableName
        params["dbType"] = "hbase"
        params["uri"] = "gpu0.dev.yufei.com:9999"

        batchPut(params=params)

    def test_Hbase(self):
        # imageFeatures

        puts = []
        put = {
            "c0:imageId": "1223456",
            "c1:layer4_features": "4.0,2.0,4.0,2.0,4.0,2.0,4.0,2.0",
            "c1:modelName": "fb_32_16",
        }

        puts.append(put)
        put = {"c0:imageId": "12324567"}
        puts.append(put)

        tableName = "imageFeatures_test"
        params = {}
        params["puts"] = puts
        params["tableName"] = tableName
        params["dbType"] = "hbase"
        params["uri"] = "gpu0.dev.yufei.com:9999"

        batchPut(params=params)


class MathUtilsTest(unittest.TestCase):
    def testMathUtils(self):
        import numpy as np

        from souJpg.comm.mathUtils import l2NormAndRound

        featuresStr = "1.934,23.3"
        featureArray = l2NormAndRound(
            np.asarray([featuresStr.split(",")]).astype(np.float32), norm="hellinger"
        )
        print(featureArray)
        print(LA.norm(featureArray, 2))
        featureArray1 = l2NormAndRound(np.asarray([featuresStr.split(",")]), norm="l2")
        print(LA.norm(featureArray1, 2))


class KafkaOpsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.kafkaOps = KafkaOps()
        self.topicName = "testTopic"

    def test_sendMessage(self):
        message = Message()
        message.topicName = self.topicName
        content = {}
        content["field1"] = "test"
        message.content = content
        self.kafkaOps.sendMessage(message=message)

    def test_createConsumer(self):
        consumerParams = ConsumerParams()
        consumerParams.topicName = self.topicName
        consumerParams.groupId = "testGroupId1"
        consumerParams.auto_offset_reset = "earliest"

        consumer = self.kafkaOps.createConsumer(consumerParams=consumerParams)
        succeedNum = 0
        while True:
            try:
                partionResults = consumer.poll(timeout_ms=1000)
                time.sleep(1)
                values = []
                for partionResult in partionResults.values():
                    for record in partionResult:
                        value = record.value
                        values.append(value)
                succeedNum += len(values)
                print("batch size:%d" % len(values))
                for value in values:
                    try:
                        s = value.decode("utf-8")
                        content = str(json.loads(s))
                        logger1.info("consume message:{}", content)

                    except BaseException as e:
                        print(value)

            except BaseException as e:
                print("error to process: " + str(e))
            consumer.commit_async()

        consumer.close(autocommit=True)

    def test_consume(self):
        consumerParams = ConsumerParams()
        consumerParams.topicName = self.topicName
        consumerParams.groupId = "testGroupId1"
        consumerParams.auto_offset_reset = "earliest"
        consumerParams.updatedOffset = 4
        consumerParams.partitionNum = 0

        consumer = self.kafkaOps.createConsumer(consumerParams=consumerParams)

        def batchMessageHandler(messages):
            for message in messages:
                logger1.info(
                    "consumer: {}, message: {}, keys: {}",
                    consumerParams.topicName,
                    message,
                    message.keys(),
                )

        self.kafkaOps.consume(
            consumer=consumer, batchMessageHandler=batchMessageHandler
        )


class DistributeFsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.fs = MinioFs()
        self.cosFs=TecentCosFs()

    def test_upload(self):
        localFile = r"C:\Users\jasstion\OneDrive\图片\sexy\屏幕截图 2022-07-04 095052.jpg"
        self.fs.upload(
            localFilePath=localFile,
            remoteFilePath="images/souJpg/illegal/test2.jpg",
            deleteLocal=False,
        )

    def test_uploadFolder(self):
        localFile = r"C:\Users\jasstion\OneDrive\图片\Saved Pictures"
        self.fs.uploadFolder(
            localFolderPath=localFile,
            remoteFolderPath="images/testImages",
            deleteLocal=False,
        )

    def test_download(self):
        localFile = r"C:\Users\jasstion\OneDrive\图片\12.jpg"
        self.fs.download(
            localFilePath=localFile, remoteFilePath="images/testImages/sexy/test1.jpg"
        )

    def test_downloadFolder(self):
        localFolderPath = r"C:\Users\jasstion\test"
        self.fs.downloadFoler(
            localFolderPath=localFolderPath, remoteFolderPath="images/testImages"
        )
    def test_upload_cos(self):
        localFile = "/data3/mlib_data/zhaoyufei_cache/loras_test/Remv2FB.safetensors"
        self.cosFs.upload(
            localFilePath=localFile,
            remoteFilePath="models/loras_test/",
            deleteLocal=False,
        )

    def test_uploadFolder_cos(self):
        localFile = r"/data3/mlib_data/zhaoyufei_cache/loras_test/"
        self.cosFs.uploadFolder(
            localFolderPath=localFile,
            remoteFolderPath="models/loras_test/",
            deleteLocal=False,
        )

    def test_download_cos(self):
        localFile = "/data3/mlib_data/loras_test/Remv2FB.safetensors"
        self.cosFs.download(
            localFilePath=localFile, remoteFilePath="models/loras_test/Remv2FB.safetensors"
        )

class RedisOpsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.redisOps = RedisOps()

    def test_redisOps(self):
        redisOps = self.redisOps
        keydict = {
            "1": "12_1 34_2 45_3 88_4",
            "2": "120_1 3_2 4_3 88_4",
            "3": "11_1 4_2 234_3 88_4",
        }
        redisOps.mset(keydict=keydict)
        keys = ["1", "2", "3", "euemCssxRJ7Watpb7RCjXj"]
        logger1.info(redisOps.mget(keys=keys))
        userKey = "userId"
        redisOps.set(key=userKey, value=userKey, ex=2)
        logger1.info(redisOps.get(userKey))
        time.sleep(3)
        logger1.info(redisOps.get(userKey))
        queueName = "testQueue"
        redisOps.lpush(key=queueName, value=1)
        redisOps.lpush(key=queueName, value=2)
        logger1.info(redisOps.rpop(key=queueName))
        logger1.info(redisOps.rpop(key=queueName))

        bfName = "cuckoo2"
        redisOps.bfPush(bfName, "1")
        redisOps.bfPush(bfName, "1000")
        redisOps.bfPush(bfName, "1")
        logger1.info(redisOps.bfExist(bfName, "1"))
        logger1.info(redisOps.bfExist(bfName, "10"))

    def test_cache(self):
        @cached(ex=4)
        def testFunc(a, b):
            logger1.info("compute: {} + {}", a, b)
            return {"sum": a + b}

        # if result is None will not cache
        @cached(ex=4)
        def testNoneFunc(a, b):
            return None

        sum = testFunc(10, 11)
        
        logger1.info("sum: {}", sum)
        sum = testFunc(10, 1)
        logger1.info("sum: {}", sum)
        sum = testNoneFunc(10, 1)
        sum = testFunc(100, 1)

        logger1.info("sum: {}", sum)


def cleanTmpImagesFolder(tmpImagesFolder):
    with ExceptionCatcher():
        shutil.rmtree(tmpImagesFolder, ignore_errors=True)

        logger1.info("delete temporary local folder: {}", tmpImagesFolder)
        os.makedirs(tmpImagesFolder)


class VideoUtilsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.videoUrl = "https://soujpg-videos-1307121509.cos.ap-beijing.myqcloud.com/VCG42686869508.mp4"

    def test_parseVideo(self):
        cleanTmpImagesFolder("./tmp")
        result = parseVideo(videoUrl=self.videoUrl)
        logger1.info(result)
        frameBytes = result.frameImageBytes
        logger1.info("frameBytes: {}", type(frameBytes))
        logger1.info("frameBytes: {}", len(frameBytes))
        for frameImageBytes in frameBytes:
            with pil_image.open(io.BytesIO(frameImageBytes)) as img:
                img.save("./tmp/{}.jpg".format(uuid.uuid4().hex))
        # cleanTmpImagesFolder("./tmp")
class ContextManagerTest(unittest.TestCase):
    def setUp(self) -> None:
        pass
    def test_methodRetryWraper(self):
        @methodRetryWraper(maxAttempts=2)
        def testFunc():
            logger1.info("testFunc")
            # raise Exception("test exception")
        testFunc()
        


if __name__ == "__main__":
    unittest.main()
    # urls = [
    #     # "http://gpu0.dev.yufei.com:8005/image/images_picJumpo/QEXVE3eQ7BBNrrZBtJ9i4z/",
    #     # "https://images-1307121509.cos.ap-beijing.myqcloud.com/souJpg/images/MrW4YjVdtHryu7TjCXq3Fx.jpg",
    #     "https://images-1307121509.cos.ap-beijing.myqcloud.com/souJpg/images/6Xj78uckHaWkqF9FWF3qTe.jpg",
    # ]
    # for url in urls:
    #     imageBytes = imageUtils.resizeAndBytesImageFromUrl(imageUrl=url)
    #     with pil_image.open(io.BytesIO(imageBytes)) as img:
    #         if img.mode != "RGB":
    #             img = img.convert("RGB")
    #         img.show()
    #         logger1.info(img.size)

    #     resolution, previewBytes, mediumBytes, largeBytes = imageUtils.imagesMaker(
    #         imageBytes=imageBytes
    #     )
    #     logger1.info(resolution)
    #     for image in [previewBytes, mediumBytes, largeBytes]:
    #         with pil_image.open(io.BytesIO(image)) as img:
    #             if img.mode != "RGB":
    #                 img = img.convert("RGB")
    #             img.show()
    #             logger1.info(img.size)
    #             logger1.info(img.size)
