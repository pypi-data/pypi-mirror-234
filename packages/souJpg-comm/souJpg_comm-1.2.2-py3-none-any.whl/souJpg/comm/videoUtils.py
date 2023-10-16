import os
import shutil
import sys
from typing import List, Optional

import cv2
from loguru import logger as logger1
from PIL import Image as pil_image
from pydantic import BaseModel

from souJpg.comm.contextManagers import ExceptionCatcher
from souJpg.comm.imageUtils import *


# FPS: 25.0, Width: 1364, Height: 720, Frame count: 375
class VideoParsedResult(BaseModel):
    fps: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    frameCount: Optional[int] = None
    # 每隔25 frame 采集一个frame
    sampledFrameRate: Optional[int] = 25
    frameImageBytes: Optional[List[bytes]] = None


def parseVideo(videoUrl=None, sampledFrameRate=25):
    videoParsedResult = VideoParsedResult()
    # 打开视频文件
    cap = cv2.VideoCapture(videoUrl)
    frameImageBytes = []

    # 获取视频属性
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 解析视频文件，将每一帧作为图像输出
    frame_idx = -1
    while cap.isOpened():
        # 读取视频帧

        ret, frame = cap.read()
        frame_idx += 1
        if frame_idx % sampledFrameRate != 0:
            continue
        logger1.info(f"frame_idx: {frame_idx}")

        # 如果视频结束，跳出循环
        if not ret:
            break
        # convert frame to pil image
        framePilImage = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        newImageBytes = io.BytesIO()
        framePilImage.save(newImageBytes, format="jpeg", quality=75)
        newImageBytes = newImageBytes.getvalue()
        frameImageBytes.append(newImageBytes)

        # 释放资源
    cap.release()
    videoParsedResult.fps = fps
    videoParsedResult.width = width
    videoParsedResult.height = height
    videoParsedResult.frameCount = frameCount
    videoParsedResult.frameImageBytes = frameImageBytes
    return videoParsedResult
