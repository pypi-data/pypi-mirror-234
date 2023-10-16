import abc
from enum import Enum
import io
import shortuuid
from loguru import logger
from pymongo import UpdateOne
from qcloud_cos import CosConfig, CosS3Client
from souJpg.comm import imageUtils
from souJpg.comm.contextManagers import ExceptionCatcher
from souJpg.comm.dbHelper import createMongoDBConnection
from souJpg.comm.utils import singleton
from PIL import Image
from souJpg import gcf


class ResolutionType(Enum):
    preview = "preview"
    medium = "medium"
    large = "large"
    # 采集到的原图
    original = "original"
    # 初次采集到的图的尺寸
    stardard = "stardard"


resolutions = [
    ResolutionType.preview,
    ResolutionType.medium,
    ResolutionType.large,
    ResolutionType.original,
    ResolutionType.stardard,
]


class ImageStoreService:
    def __init__(self, cfg={}) -> None:
        self.cfg = cfg

    @abc.abstractmethod
    def generateUrl(
        self,
        source=None,
        imageId=None,
        format="jpg",
        resolution=ResolutionType.preview,
        domain=None,
        ssl=False,
    ):
        pass

    @abc.abstractmethod
    def uploadImage(
        self,
        source=None,
        imageId=None,
        format="jpg",
        imageBase64Str=None,
        resolution=ResolutionType.original,
    ):
        """
        upload original image data and return if success
        supported image type: jpg, png, webp, jpeg
        Here need resolution parameter? No, because we will need to upload original image data

        """
        pass

    @abc.abstractmethod
    def downloadImage(
        self,
        imageName: str,
    ):
        """
        download image from private or public cos buckets
        imageName contains imageId and format
        """
        pass

    @abc.abstractmethod
    def makeDiffResolutionTypeImages(self, source=None, imageId=None, format="jpg"):
        """
        Any format will be convert to jpg, then make diff resolution type images
        """
        pass


class MongodbImageStoreService(ImageStoreService):
    def __init__(self, cfg={}) -> None:
        super().__init__(cfg=cfg)

        self.imageServerPort = cfg.get("imageServerPort", gcf.imageServerPort)
        self.imageServerDomain = cfg.get("imageServerDomain", gcf.imageServerDomain)

        self.imagesDBConnection = createMongoDBConnection(dbType="images")

    def generateUrl(
        self,
        source=None,
        imageId=None,
        format="jpg",
        resolution=ResolutionType.preview,
        domain=None,
        ssl=False,
    ):
        privateUrlTemplate = None
        if domain is None:
            domain = self.imageServerDomain
        if ssl:
            privateUrlTemplate = "https://%s:%s/image/{tableName}/{imageId}/" % (
                domain,
                str(self.imageServerPort),
            )
        else:
            privateUrlTemplate = "http://%s:%s/image/{tableName}/{imageId}/" % (
                domain,
                str(self.imageServerPort),
            )
        assert resolution in resolutions
        resolution = resolution.value
        url = None
        tableName = None

        # images-> source
        if resolution == ResolutionType.stardard.value:
            tableName = "%s_%s" % ("images", source)
        else:
            tableName = "%s_%s-%s" % ("images", source, resolution)
        if tableName is None or imageId is None:
            logger.info("source:{},imageId:{} error ", source, imageId)
        url = privateUrlTemplate.replace("{tableName}", tableName).replace(
            "{imageId}", imageId
        )
        return url

    def uploadImage(
        self,
        source=None,
        imageId=None,
        format="jpg",
        imageBase64Str=None,
        resolution=ResolutionType.original,
    ):
        succeed = False

        with ExceptionCatcher() as ec:
            if resolution == ResolutionType.original:
                tableName = "%s" % (source)
            else:
                tableName = "%s-%s" % (source, resolution.value)

            imagesTable = self.imagesDBConnection[tableName]
            document = {}
            document["content"] = imageBase64Str
            action = UpdateOne(
                filter={"imageId": imageId},
                update={"$set": document},
                upsert=True,
            )

            bulk_writeR = imagesTable.bulk_write([action])
            logger.info(bulk_writeR.bulk_api_result)
        if ec.error is None:
            succeed = True

        return succeed

    def makeDiffResolutionTypeImages(self, source=None, imageId=None, format="jpg"):
        succeed = False
        resolution = None
        with ExceptionCatcher() as ec:
            imageInfo = self.imagesDBConnection[source].find_one({"imageId": imageId})
            imageBase64Str = imageInfo.get("content")
            imageBytes = imageUtils.imageBase642ImageBytes(imageBase64=imageBase64Str)

            (
                resolution,
                previewBytes,
                mediumBytes,
                largeBytes,
            ) = imageUtils.imagesMaker(imageBytes=imageBytes)
            for resolution, image in zip(
                ["preview", "medium", "large"],
                [previewBytes, mediumBytes, largeBytes],
            ):
                document = {}
                document["content"] = imageUtils.imageBytes2Base64(imageBytes=image)
                action = UpdateOne(
                    filter={"imageId": imageId},
                    update={"$set": document},
                    upsert=True,
                )

                bulk_writeR = self.imagesDBConnection[
                    "%s-%s" % (source, resolution)
                ].bulk_write([action])
                logger.info(bulk_writeR.bulk_api_result)
        if ec.error is None:
            succeed = True

        return (succeed, resolution)


class TencentCosImageStoreService(ImageStoreService):
    """
    support image format,like: webp,jpeg/jpg,png

    Args:
        ImageStoreService (_type_): _description_


     imageName: imageId + format
     image url:   imageBucketName,region,imageKeyPrefix,imageId,format



    """

    def __init__(self, cfg={}) -> None:
        super(TencentCosImageStoreService, self).__init__(cfg=cfg)

        self.secret_id = cfg.get("secret_id", gcf.tencent_secret_id)
        self.secret_key = cfg.get("secret_key", gcf.tencent_secret_key)
        self.region = cfg.get("region", gcf.tencent_region)
        self.imageBucketName = cfg.get("imageBucketName", gcf.tencent_imageBucketName)
        # bucket sub folder path
        self.imageKeyPrefix = cfg.get("imageKeyPrefix", gcf.tencent_imageKeyPrefix)

        token = None
        scheme = "https"

        config = CosConfig(
            Region=self.region,
            SecretId=self.secret_id,
            SecretKey=self.secret_key,
            Token=token,
            Scheme=scheme,
        )
        self.client = CosS3Client(config)

        self.cosUrlTemplate = (
            "https://{imageBucketName}.cos.{region}.myqcloud.com/{imageKeyPrefix}{imageId}.{format}".replace(
                "{imageBucketName}", self.imageBucketName
            )
            .replace("{region}", self.region)
            .replace("{imageKeyPrefix}", self.imageKeyPrefix)
        )

    def generateUrl(
        self,
        source=None,
        imageId=None,
        format="webp",
        resolution=ResolutionType.preview,
        domain=None,
        ssl=gcf.imageUrlssl,
    ):
        assert resolution in resolutions
        if resolution != ResolutionType.original:
            imageIdKey = shortuuid.uuid(
                name="%s_%s_%s" % (source, imageId, resolution.value)
            )
        else:
            imageIdKey = shortuuid.uuid(name="%s_%s" % (source, imageId))

        url = self.cosUrlTemplate.replace("{imageId}", imageIdKey).replace(
            "{format}", format
        )
        return url

    def uploadImage(
        self,
        source=None,
        imageId=None,
        format="jpg",
        imageBase64Str=None,
        resolution=ResolutionType.original,
    ):
        """
        if format is None, then use imageBase64Str to detect format
        L,RGBA,RGB
        if format is not None, then just use format

        Returns:
            boolean: succeed
        """
        succeed = False
        with ExceptionCatcher() as ec:
            assert imageBase64Str is not None
            if resolution == ResolutionType.original:
                imageIdKey = shortuuid.uuid(name="%s_%s" % (source, imageId))
            else:
                imageIdKey = shortuuid.uuid(
                    name="%s_%s_%s" % (source, imageId, resolution.value)
                )

            imageBytes = imageUtils.imageBase642ImageBytes(imageBase64=imageBase64Str)
            if format is None:
                with Image.open(io.BytesIO(imageBytes)) as img:
                    mode = img.mode
                if mode == "RGBA":
                    format = "png"
                else:
                    format = "jpg"

            key = "%s%s.%s" % (self.imageKeyPrefix, imageIdKey, format)

            response = self.client.put_object(
                Bucket=self.imageBucketName,
                Body=imageBytes,
                Key=key,
                StorageClass="STANDARD",
                ContentType="image/%s" % format,
            )
            logger.info(response)
        if ec.error is None:
            succeed = True
        return succeed

    def makeDiffResolutionTypeImages(self, source=None, imageId=None, format="jpg"):
        succeed = False
        resolution = None
        with ExceptionCatcher() as ec:
            originalUrl = self.generateUrl(
                source=source,
                imageId=imageId,
                resolution=ResolutionType.original,
                ssl=gcf.imageUrlssl,
                format=format,
            )
            logger.debug(
                "get originalUrl: {}, source: {}, imageId: {} ",
                originalUrl,
                source,
                imageId,
            )

            imageBytes = imageUtils.resizeAndBytesImageFromUrl(imageUrl=originalUrl)

            (
                resolution,
                previewBytes,
                mediumBytes,
                largeBytes,
            ) = imageUtils.imagesMaker(imageBytes=imageBytes)
            for resolution, imageBytes in zip(
                ["preview", "medium", "large"],
                [previewBytes, mediumBytes, largeBytes],
            ):
                imageIdKey = shortuuid.uuid(
                    name="%s_%s_%s" % (source, imageId, resolution)
                )
                key = "%s%s%s" % (self.imageKeyPrefix, imageIdKey, ".jpg")

                logger.debug(
                    "original url: {}, {} imageIdKey: {}", originalUrl, resolution, key
                )

                response = self.client.put_object(
                    Bucket=self.imageBucketName,
                    Body=imageBytes,
                    Key=key,
                    StorageClass="STANDARD",
                    ContentType="image/jpeg",
                )
                logger.info(response)

        if ec.error is None:
            succeed = True

        return (succeed, resolution)

    # given source and imageId，delete image from imageStoreService
    def deleteImage(self, source=None, imageId=None, format="webp"):
        succeed = False
        with ExceptionCatcher() as ec:
            for resolution in resolutions:
                if resolution != ResolutionType.original:
                    imageIdKey = shortuuid.uuid(
                        name="%s_%s_%s" % (source, imageId, resolution.value)
                    )
                else:
                    imageIdKey = shortuuid.uuid(name="%s_%s" % (source, imageId))
                key = "%s%s.%s" % (self.imageKeyPrefix, imageIdKey, format)
                logger.debug("delete image key: {}", key)
                response = self.client.delete_object(
                    Bucket=self.imageBucketName,
                    Key=key,
                )
                logger.info(response)
        if ec.error is None:
            succeed = True
        return succeed

    def uploadImageUingTmpKeys(
        self,
        imageBase64Str=None,
        fileName=None,
        temp_secret_id=None,
        temp_secret_key=None,
        temp_token=None,
        format="jpg",
    ):
        token = temp_token
        scheme = "https"
        imageBytes = imageUtils.imageBase642ImageBytes(imageBase64=imageBase64Str)
        config = CosConfig(
            Region=self.region,
            SecretId=temp_secret_id,
            SecretKey=temp_secret_key,
            Token=token,
            Scheme=scheme,
        )
        client = CosS3Client(config)
        response = client.put_object(
            Bucket=self.imageBucketName,
            Body=imageBytes,
            Key="%s%s" % (self.imageKeyPrefix, fileName),
            StorageClass="STANDARD",
            ContentType="image/%s" % format,
        )
        logger.info(response)

    def downloadImageUingTmpKeys(
        self, fileName=None, temp_secret_id=None, temp_secret_key=None, temp_token=None
    ):
        response = None
        image = None
        image_bytes = b""
        with ExceptionCatcher() as ec:
            token = temp_token
            scheme = "https"

            config = CosConfig(
                Region=self.region,
                SecretId=temp_secret_id,
                SecretKey=temp_secret_key,
                Token=token,
                Scheme=scheme,
            )
            client = CosS3Client(config)

            # 下载图片
            response = client.get_object(
                Bucket=self.imageBucketName,
                Key="%s%s" % (self.imageKeyPrefix, fileName),
            )
            for chunk in response["Body"].get_stream():
                image_bytes += chunk
            # image = Image.open(io.BytesIO(image_bytes))

        return image_bytes

    def downloadImage(
        self,
        imageName: str,
    ):
        """
        download image from private or public cos buckets
        """
        # image = None
        image_bytes = b""
        with ExceptionCatcher() as ec:

            logger.debug("download image key: {}", imageName)
            response = self.client.get_object(
                Bucket=self.imageBucketName,
                Key="%s%s" % (self.imageKeyPrefix, imageName),
            )
            logger.info(response)
            for chunk in response["Body"].get_stream():
                image_bytes += chunk
            # image = Image.open(io.BytesIO(image_bytes))
        return image_bytes


def createImageStoreService(imageStoreServiceKey=None):
    logger.debug("imageStoreServiceKey: {}", imageStoreServiceKey)
    imageStoreService = None
    if imageStoreServiceKey is None:
        imageStoreServiceKey = gcf.imageStoreServiceKey

    if imageStoreServiceKey == "mongodb":
        imageStoreService = MongodbImageStoreService()
    elif imageStoreServiceKey == "tencentCos":
        imageStoreService = TencentCosImageStoreService()
    elif imageStoreServiceKey == "tencentCosTmp":
        cfg = {
            "region": gcf.tencent_region_userUpload,
            "imageBucketName": gcf.tencent_imageBucketName_userUpload,
            "imageKeyPrefix": "tmp/",
        }

        imageStoreService = TencentCosImageStoreService(cfg=cfg)
    elif imageStoreServiceKey == "tencentCosPrivate":
        cfg = {
            "region": "ap-nanjing",
            "imageBucketName": "soujpg-private-1307121509",
            "imageKeyPrefix": "ai-image/",
            "secret_id": "AKIDPgylS0Qdcs495yhKtJbl095pXBqMhrsL",
            "secret_key": "MZoxsZBbwHUYeaH0fDdv2EMas3DIBvjl",
        }

        imageStoreService = TencentCosImageStoreService(cfg=cfg)
    else:
        raise Exception("not valid imageStoreServiceKey")
    return imageStoreService
