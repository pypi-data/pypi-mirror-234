import base64
import sys
import uuid

import shortuuid
from loguru import logger as logger1
from qcloud_cos import CosConfig, CosS3Client
from souJpg import gcf
from souJpg.comm.dbsCL import MongoCL
from souJpg.comm.imageUtils import *


class CosOps(object):
    def __init__(self):
        secret_id = gcf.tencent_secret_id # 替换为用户的 SecretId，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
        secret_key = gcf.secret_key  # 替换为用户的 SecretKey，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
        region = "ap-beijing"  # 替换为用户的 region，已创建桶归属的region可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
        # COS支持的所有region列表参见https://cloud.tencent.com/document/product/436/6224
        token = None  # 如果使用永久密钥不需要填入token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见https://cloud.tencent.com/document/product/436/14048
        scheme = "https"  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

        config = CosConfig(
            Region=region,
            SecretId=secret_id,
            SecretKey=secret_key,
            Token=token,
            Scheme=scheme,
        )
        self.client = CosS3Client(config)
        self.imageBucketName = "images-1307121509"
        self.imageKeyPrefix = "souJpg/images/"

    def pushImage(self, imageBytes=None, imageId=None, source=None):
        imageIdKey = shortuuid.uuid(name="%s_%s" % (source, imageId))
        key = "%s%s-" % (self.imageKeyPrefix, imageIdKey, ".jpg")

        response = self.client.put_object(
            Bucket=self.imageBucketName,
            Body=imageBytes,
            Key=key,
            StorageClass="STANDARD",
            ContentType="image/jpeg",
        )
        logger1.info(response)
