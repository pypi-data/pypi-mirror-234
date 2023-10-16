from __future__ import absolute_import, division, print_function
import copy
from pydantic import BaseModel
from typing import List, Optional
from sts.sts import Sts
from souJpg.comm.apiResponse import BaseResponse, ErrorCodeType
from souJpg.comm.contextManagers import ExceptionCatcher
from souJpg import gcf


class TencentCosCredential(BaseModel):
    credentials: Optional[dict] = None


class CosKeyService:
    def __init__(self) -> None:
        self.buketName2Sts = {}
        with ExceptionCatcher() as ec:
            baseConfig = {
                "url": "https://sts.tencentcloudapi.com/",
                "domain": "sts.tencentcloudapi.com",
                "duration_seconds": 1800,
                "secret_id": "AKIDlIdle8YlncCg9Vi19IFwiKTk1JTk7PYp",
                "secret_key": "DJOPJxW6YDerukLI9zkMo6UinkcJ1d1D",
                "allow_prefix": ["*"],
            }
            userUploadBucketStsConfig = copy.deepcopy(baseConfig)

            bucketName = gcf.tencent_imageBucketName_userUpload
            region = gcf.tencent_region_userUpload

            userUploadBucketStsConfig["bucket"] = bucketName
            userUploadBucketStsConfig["region"] = region
            userUploadBucketStsConfig["allow_actions"] = (
                [
                    # 简单上传
                    "name/cos:PutObject",
                    "name/cos:PostObject",
                    # 分片上传
                    "name/cos:InitiateMultipartUpload",
                    "name/cos:ListMultipartUploads",
                    "name/cos:ListParts",
                    "name/cos:UploadPart",
                    "name/cos:CompleteMultipartUpload",
                ],
            )
            policy = {
                "version": "2.0",
                "statement": [
                    {
                        "action": ["name/cos:PutObject"],
                        "effect": "allow",
                        "resource": ["*"],
                    }
                ],
            }
            userUploadBucketStsConfig["policy"] = policy

            sts = Sts(userUploadBucketStsConfig)

            self.buketName2Sts["%s_%s" % (region, bucketName)] = sts

            privateBucketStsConfig = copy.deepcopy(baseConfig)

            bucketName = "soujpg-private-1307121509"
            region = "ap-nanjing"

            privateBucketStsConfig["bucket"] = bucketName
            privateBucketStsConfig["region"] = region
            privateBucketStsConfig["secret_id"] = "AKIDPgylS0Qdcs495yhKtJbl095pXBqMhrsL"
            privateBucketStsConfig["secret_key"] = "MZoxsZBbwHUYeaH0fDdv2EMas3DIBvjl"
            privateBucketStsConfig["allow_actions"] = (
                [
                    # 简单上传
                    "name/cos:GetObject",
                    "name/cos:PutObject",
                ],
            )
            policy = {
                "version": "2.0",
                "statement": [
                    {
                        "action": ["name/cos:GetObject", "name/cos:PutObject"],
                        "effect": "allow",
                        "resource": ["*"],
                    }
                ],
            }
            privateBucketStsConfig["policy"] = policy
            sts = Sts(privateBucketStsConfig)

            self.buketName2Sts["%s_%s" % (region, bucketName)] = sts

    def generateTempKey(self, params=None):
        tencentCosCredential = TencentCosCredential()

        with ExceptionCatcher() as ec:
            bucketName = gcf.tencent_imageBucketName_userUpload
            region = gcf.tencent_region_userUpload
            bucketName = params.get("bucketName", "%s_%s" % (region, bucketName))
            sts = self.buketName2Sts.get(bucketName, None)

            response = sts.get_credential()
            # response = json.dumps(dict(response), indent=4)
            response = dict(response)
            tencentCosCredential.credentials = response

        return tencentCosCredential
