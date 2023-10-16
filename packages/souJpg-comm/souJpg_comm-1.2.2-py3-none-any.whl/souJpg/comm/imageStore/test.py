import io
import random
import sys
import unittest
from datetime import datetime
from loguru import logger
from PIL import Image
import pymongo
import shortuuid
from souJpg.comm import imageUtils
from souJpg.comm.dbsCL import batchPut
from souJpg.comm.imageStore.cosKeyService import CosKeyService
from souJpg.comm.imageStore.imageStoreService import (
    MongodbImageStoreService,
    ResolutionType,
    createImageStoreService,
)
from souJpg import gcf


logger.remove()
logger.add(sys.stderr, level="DEBUG")


class MongodbImageStoreServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.mongodbImageStoreService = MongodbImageStoreService()

    def test_generateUrl(self):
        resolutions = [
            ResolutionType.preview,
            ResolutionType.medium,
            ResolutionType.large,
            ResolutionType.stardard,
        ]
        source = "unsplash"
        imageId = "Lwuc40AQORI"
        domain = "gpu0.dev.yufei.com"
        for resolution in resolutions:
            url = self.mongodbImageStoreService.generateUrl(
                resolution=resolution,
                source=source,
                imageId=imageId,
                domain=domain,
                ssl=False,
            )
            logger.info(url)
            self.assertTrue(not "https" in url)
            imageBytes = imageUtils.resizeAndBytesImageFromUrl(imageUrl=url)
            self.assertTrue(imageBytes is not None)

        source = "pxhere"
        imageId = "546650"
        for resolution in resolutions:
            url = self.mongodbImageStoreService.generateUrl(
                resolution=resolution,
                source=source,
                imageId=imageId,
                domain="www.yufei-dev.com",
                ssl=True,
            )
            logger.info(url)
            self.assertTrue("https" in url)

    def test_uploadImage(self):
        source = "userUpload"
        imageId = shortuuid.uuid()
        testImageUrl = (
            "http://gpu0.dev.yufei.com:8005/image/images_pxhere-large/546650/"
        )
        imageBase64Str = imageUtils.imageBytes2Base64(
            imageBytes=imageUtils.resizeAndBytesImageFromUrl(imageUrl=testImageUrl)
        )
        succeed = self.mongodbImageStoreService.uploadImage(
            source=source, imageId=imageId, imageBase64Str=imageBase64Str
        )
        self.assertEqual(succeed, True)
        url = self.mongodbImageStoreService.generateUrl(
            source=source, imageId=imageId, resolution=ResolutionType.original
        )
        logger.info(url)
        imageBytes = imageUtils.resizeAndBytesImageFromUrl(imageUrl=url)
        self.assertTrue(imageBytes is not None)
        self.mongodbImageStoreService.makeDiffResolutionTypeImages(
            source=source, imageId=imageId
        )
        for resolutionType in resolutions:
            url = self.mongodbImageStoreService.generateUrl(
                source=source, imageId=imageId, resolution=resolutionType
            )
            logger.info(url)
            imageBytes = imageUtils.resizeAndBytesImageFromUrl(imageUrl=url)
            self.assertTrue(imageBytes is not None)

    def test_makeDiffResolutionTypeImages(self):
        source = "userUpload"
        imageId = "Y6aYKruJzMT3MnrKhaF2S9"
        self.mongodbImageStoreService.makeDiffResolutionTypeImages(
            source=source, imageId=imageId
        )


class TencentCosImageStoreServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        privateImageStoreServiceKey = "tencentCosPrivate"
        imageStoreServiceKey = "tencentCos"
        self.imageStoreService = createImageStoreService(
            imageStoreServiceKey=imageStoreServiceKey
        )

        self.privateImageStoreService = createImageStoreService(
            imageStoreServiceKey=privateImageStoreServiceKey
        )
        self.source = "pxhere"
        self.imageId = "546650"

        self.cosKeyService = CosKeyService()

    def test_generateUrl(self):
        resolutions = [
            ResolutionType.preview,
            ResolutionType.medium,
            ResolutionType.large,
        ]

        domain = "gpu0.dev.yufei.com"
        for resolution in resolutions:
            url = self.imageStoreService.generateUrl(
                resolution=resolution,
                source=self.source,
                imageId=self.imageId,
                domain=domain,
                ssl=False,
            )
            logger.info(url)
            # self.assertTrue("https" in url)
            # imageBytes = imageUtils.resizeAndBytesImageFromUrl(imageUrl=url)
            # self.assertTrue(imageBytes is not None)

        for resolution in resolutions:
            url = self.imageStoreService.generateUrl(
                resolution=resolution,
                source=self.source,
                imageId=self.imageId,
                domain="www.yufei-dev.com",
                ssl=gcf.imageUrlssl,
            )
            logger.info(url)
            self.assertTrue("https" in url)

            # imageBytes = imageUtils.resizeAndBytesImageFromUrl(imageUrl=url)
            # # logger.info(imageBytes)
            # self.assertTrue(imageBytes is not None)

    def test_uploadImage(self):
        source = "userUpload"
        imageId = shortuuid.uuid()
        testImageUrl = (
            "https://assets.soujpg.com/souJpg/images/RNA3iv775sv9yi86FdLtLm.webp"
        )
        imageBase64Str = imageUtils.imageBytes2Base64(
            imageBytes=imageUtils.resizeAndBytesImageFromUrl(imageUrl=testImageUrl)
        )
        succeed = self.imageStoreService.uploadImage(
            source=source, imageId=imageId, imageBase64Str=imageBase64Str, format="webp"
        )
        self.assertEqual(succeed, True)
        url = self.imageStoreService.generateUrl(
            source=source,
            imageId=imageId,
            resolution=ResolutionType.original,
            format="webp",
        )
        logger.info(url)
        imageBytes = imageUtils.resizeAndBytesImageFromUrl(imageUrl=url)
        self.assertTrue(imageBytes is not None)

    def test_uploadImageUsingTmpKeys(self):
        tencentCosCredential = self.cosKeyService.generateTempKey(
            params={"bucketName": "ap-nanjing_soujpg-private-1307121509"}
        )
        logger.info(tencentCosCredential)
        temp_secret_id = tencentCosCredential.credentials["credentials"]["tmpSecretId"]
        temp_secret_key = tencentCosCredential.credentials["credentials"][
            "tmpSecretKey"
        ]
        temp_token = tencentCosCredential.credentials["credentials"]["sessionToken"]
        testImageUrl = (
            "https://assets.soujpg.com/souJpg/images/RNA3iv775sv9yi86FdLtLm.webp"
        )
        imageBase64Str = imageUtils.imageBytes2Base64(
            imageBytes=imageUtils.resizeAndBytesImageFromUrl(imageUrl=testImageUrl)
        )

        response = None

        response = self.privateImageStoreService.uploadImageUingTmpKeys(
            imageBase64Str=imageBase64Str,
            fileName="test.jpg",
            temp_secret_id=temp_secret_id,
            temp_secret_key=temp_secret_key,
            temp_token=temp_token,
        )
        logger.info(response)

        # test download image directly
        response = self.privateImageStoreService.downloadImage(
            imageName="test.jpg",
        )
        response = Image.open(io.BytesIO(response))
        response.save("output.jpg")

    def test_makeDiffResolutionTypeImages(self):
        source = "userUpload"
        imageId = "Y6aYKruJzMT3MnrKhaF2S9"
        self.imageStoreService.makeDiffResolutionTypeImages(
            source=source, imageId=imageId
        )

    def test_deleteImage(self):
        source = "userUpload"
        imageId = "VbToiQbqdqnkqKGCQo5azc"
        self.imageStoreService.deleteImage(
            source=source, imageId=imageId, format="webp"
        )

    def test_downloadFileUingTmpKeys(self):

        source = "userUpload"
        imageId = shortuuid.uuid()
        testImageUrl = (
            "https://assets.soujpg.com/souJpg/images/RNA3iv775sv9yi86FdLtLm.webp"
        )
        imageBase64Str = imageUtils.imageBytes2Base64(
            imageBytes=imageUtils.resizeAndBytesImageFromUrl(imageUrl=testImageUrl)
        )
        succeed = self.privateImageStoreService.uploadImage(
            source=source, imageId=imageId, imageBase64Str=imageBase64Str, format="webp"
        )
        self.assertEqual(succeed, True)
        url = self.imageStoreService.generateUrl(
            source=source,
            imageId=imageId,
            resolution=ResolutionType.original,
            format="webp",
        )
        imageKey = url.split("/")[-1]
        logger.info(imageKey)

        tencentCosCredential = self.cosKeyService.generateTempKey(
            params={"bucketName": "ap-nanjing_soujpg-private-1307121509"}
        )
        logger.info(tencentCosCredential)
        temp_secret_id = tencentCosCredential.credentials["credentials"]["tmpSecretId"]
        temp_secret_key = tencentCosCredential.credentials["credentials"][
            "tmpSecretKey"
        ]
        temp_token = tencentCosCredential.credentials["credentials"]["sessionToken"]

        response = self.privateImageStoreService.downloadImageUingTmpKeys(
            fileName=imageKey,
            temp_secret_id=temp_secret_id,
            temp_secret_key=temp_secret_key,
            temp_token=temp_token,
        )
        logger.info(response)
        response.save("output.jpg")

        # test download image directly
        response = self.privateImageStoreService.downloadImage(
            imageName=imageKey,
        )
        logger.info(response)
        response.save("output1.jpg")


if __name__ == "__main__":
    unittest.main()
