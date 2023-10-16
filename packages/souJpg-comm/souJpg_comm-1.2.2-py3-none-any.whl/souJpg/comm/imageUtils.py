import base64
import io
import os
import ssl
import sys
import tempfile
import time
import traceback
import urllib.request
from io import StringIO

import cv2
import imgaug as ia
import matplotlib.pyplot as plt
import numpy as np
from imgaug import augmenters as iaa
from loguru import logger as logger1
from PIL import Image
from PIL import Image as pil_image
from PIL import ImageColor
from skimage.io import imsave
from sklearn.metrics import euclidean_distances


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray


def getImageBytesListFromFolder(folderName: str, ifRgb=True, format="JPEG"):
    _, _, testPaths = next(os.walk(folderName))

    logger1.debug(testPaths)
    imageByteses = []
    imageNames = []

    for imagePath in testPaths:
        imageNames.append(imagePath)

        imageBytes = None
        imageFullPath = folderName + imagePath
        imageBytes = resizeAndBytesImageFromPath(
            imagePath=imageFullPath,
            ifRgb=ifRgb,
            format=format,
        )
        imageByteses.append(imageBytes)
    return (imageNames, imageByteses)


def resizeImageBytes(
    imageBytes=None,
    targetSize=None,
    format="JPEG",
    ifRgb=True,
    inverse=False,
    ifSmallerNoResize=False,
    quality=75,
):
    """

    :param imageBytes:
    :param targetSize:
    :param inverse:
    :param ifSmallerNoResize: 在对query image 提取特征的时候，如果小于预期值，进行resize会破坏sift特征的准确性
    :return:
    """

    with pil_image.open(io.BytesIO(imageBytes)) as img:
        if ifRgb:
            if img.mode != "RGB":
                img = img.convert("RGB")

        rawW, rawH = img.size
        newW = rawW
        newH = rawH
        if targetSize is not None:
            if not isinstance(targetSize, list) and not isinstance(targetSize, int):
                raise Exception("targetSize can only be int or list type!")
            if isinstance(targetSize, list):
                newW, newH = targetSize
            else:
                if ifSmallerNoResize:
                    max = rawH
                    if rawH < rawW:
                        max = rawW

                    if max < targetSize:
                        logger1.debug(
                            "not to resize, for ifSmallerNoResize is True, and rawH or rawW all small then targetSize"
                        )
                        newH = rawH
                        newW = rawW
                    else:
                        newH, newW = computeNewHAndNewW(inverse, rawH, rawW, targetSize)

                else:
                    newH, newW = computeNewHAndNewW(inverse, rawH, rawW, targetSize)

            img = img.resize((int(newW), int(newH)))

        newImageBytes = io.BytesIO()
        img.save(newImageBytes, format=format, quality=quality)
        newImageBytes = newImageBytes.getvalue()
        return newImageBytes


def computeNewHAndNewW(inverse, rawH, rawW, targetSize):
    newH = None
    newW = None
    if inverse:
        if rawH > rawW:
            newH = targetSize
            # why add 1.0
            # newH = (newW / rawW) * rawH + 1.0
            newW = (newH / rawH) * rawW
        else:
            newW = targetSize
            # why add 1.0
            # newW = (newH / rawH) * rawW + 1.0
            newH = (newW / rawW) * rawH
    else:
        if rawH > rawW:
            newW = targetSize
            # why add 1.0
            # newH = (newW / rawW) * rawH + 1.0
            newH = (newW / rawW) * rawH
        else:
            newH = targetSize
            # why add 1.0
            # newW = (newH / rawH) * rawW + 1.0
            newW = (newH / rawH) * rawW
    return newH, newW


def resizeAndBytesImageFromUrl(
    imageUrl=None,
    targetSize=None,
    format="JPEG",
    ifRgb=True,
    inverse=False,
    ifSmallerNoResize=False,
):
    # image 最小边是300， 另外一个边按比例扩大
    newImageBytes = None
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        start_time = time.time()

        with urllib.request.urlopen(imageUrl, context=ctx, timeout=10) as response:
            imageBytes = response.read()
        logger1.trace(
            "spent --- %s seconds --- to download image" % (time.time() - start_time)
        )
        logger1.trace("imageBytes:{}", imageBytes)

        if targetSize is not None:
            newImageBytes = resizeImageBytes(
                imageBytes=imageBytes,
                targetSize=targetSize,
                format=format,
                ifRgb=ifRgb,
                inverse=inverse,
                ifSmallerNoResize=ifSmallerNoResize,
            )
        else:
            newImageBytes = imageBytes

    except Exception as e:
        logger1.info("error:{}", imageUrl, str(e))
        logger1.info("-" * 60)
        traceback.print_exc(file=sys.stdout)
        logger1.info("-" * 60)

    return newImageBytes


def resizeAndBytesImageFromPath(
    imagePath=None,
    targetSize=None,
    inverse=False,
    ifSmallerNoResize=False,
    ifRgb=True,
    format="JPEG",
):
    newImageBytes = None
    try:
        imageBytes = None
        with open(imagePath, "rb") as image:
            imageBytes = image.read()

        # if targetSize is not None:
        #     newImageBytes = resizeImageBytes(imageBytes=imageBytes, targetSize=targetSize, inverse=inverse,ifSmallerNoResize=ifSmallerNoResize)
        # else:
        #     newImageBytes=imageBytes
        # alwayes resizeImageBytes,if png ,resizeImageBytes have to convert from png to rgb
        newImageBytes = resizeImageBytes(
            imageBytes=imageBytes,
            targetSize=targetSize,
            format=format,
            ifRgb=ifRgb,
            inverse=inverse,
            ifSmallerNoResize=ifSmallerNoResize,
        )

    except BaseException as e:
        logger1.error(str(e))

    return newImageBytes


def splitImage(imageUrl=None, horizontalSplitParts=2, verticalSplitParts=2):
    splitsArray = []
    newImageBytes = None
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(imageUrl, context=ctx, timeout=10) as response:
            imageBytes = response.read()

        img = pil_image.open(io.BytesIO(imageBytes))
        if img.mode != "RGB":
            img = img.convert("RGB")
        img = np.array(img)
        shape = img.shape
        height = shape[0]
        width = shape[1]

        splitedHeight = int(height / verticalSplitParts)
        splitedWidth = int(width / horizontalSplitParts)

        for horizontalSplitIndex in range(0, horizontalSplitParts):
            for verticalSplitIndex in range(0, verticalSplitParts):
                startCloumns = horizontalSplitIndex * splitedWidth
                endCloumns = (horizontalSplitIndex + 1) * splitedWidth
                startRows = verticalSplitIndex * splitedHeight
                endRows = (verticalSplitIndex + 1) * splitedHeight

                block = img[startRows:endRows, startCloumns:endCloumns]
                splitsArray.append(block)

    except BaseException as e:
        print(str(e))
    return splitsArray


def grayImage(imageBytes=None):
    nparr = np.fromstring(imageBytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # newImageBytes=cv2.imencode('.jpg', img)[1].tostring()

    return img


def binaryImage(imageBytes=None, bzero=True):
    nparr = np.fromstring(imageBytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # img=cv2.GaussianBlur(img,(5,5),0)

    # ret, th = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    ret, th = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # if reverse:
    #     th1 = cv2.bitwise_not(th1)
    # zeroNum = (th == 0).sum()
    # print('zeroNum: %s' % str(zeroNum))
    # nzeroNum = (th == 255).sum()
    # print('nzeroNum: %s' % str(nzeroNum))
    # if zeroNum < nzeroNum:
    #     th = cv2.bitwise_not(th)
    if th[0, 0] == 255:
        th = cv2.bitwise_not(th)

    # newImageBytes=cv2.imencode('.jpg', th)[1].tostring()
    return th


# def imageBytes2ImageNpy(imageBytes=None):
#     img = pil_image.open(io.BytesIO(imageBytes))
#     if img.mode != "RGB":
#         img = img.convert("RGB")

#     img = np.array(img)
#     return img


def imageBytes2Base64(imageBytes=None):
    content = base64.b64encode(imageBytes)
    content = content.decode("utf-8")
    return content


def imageBase642ImageBytes(imageBase64=None):
    imageBytes = base64.b64decode(imageBase64)
    return imageBytes


# def imageNpy2ImageBytes(imageNpy=None):
#     img = pil_image.fromarray(imageNpy)
#     newImageBytes = io.BytesIO()
#     img.save(newImageBytes, format="JPEG")
#     newImageBytes = newImageBytes.getvalue()
#     return newImageBytes


def getWH(imageBytes=None):
    img = pil_image.open(io.BytesIO(imageBytes))
    w, h = img.size
    return (w, h)


def imagesMaker(imageBytes=None):
    """
    resolution: small, preview, medium, large
    small < 500*800
    preview < 1000*1500   webp
    medium  < 2000*3000  webp
    large  > 2000*3000   webp


    获取当前图片的原始分辨率，然后根据分辨率，生成不同尺寸的图片
    如果原始分辨率为preview，则medium和large都是原始分辨率，其他情况依次类推
    """
    previewBytes = None
    mediumBytes = None
    largeBytes = None
    resolution = "small"
    smallSize = 500 * 800
    previewSize = 600 * 1000
    mediumSize = 1000 * 1500
    largeSize = 2000 * 3000
    maxSize_preview = 800
    maxSize_medium = 1500
    # imageBytes = resizeImageBytes(
    #     imageBytes=imageBytes,
    #     format="webp",
    #     quality=80,
    # )
    previewQuality = 80
    size = None
    with pil_image.open(io.BytesIO(imageBytes)) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        rawW, rawH = img.size

        size = rawW * rawH

    if size >= smallSize and size <= previewSize:
        resolution = "preview"
    elif size > previewSize and size < mediumSize:
        resolution = "medium"
    elif size >= mediumSize:
        resolution = "large"

    if resolution == "preview":
        previewBytes = resizeImageBytes(
            imageBytes=imageBytes,
            format="webp",
            quality=previewQuality,
        )

        mediumBytes = imageBytes
        largeBytes = imageBytes
    if resolution == "medium":
        mediumBytes = imageBytes
        previewBytes = resizeImageBytes(
            imageBytes=imageBytes,
            inverse=True,
            targetSize=maxSize_preview,
            format="webp",
            quality=previewQuality,
        )
        largeBytes = imageBytes
    if resolution == "large":
        largeBytes = imageBytes
        previewBytes = resizeImageBytes(
            imageBytes=imageBytes,
            inverse=True,
            targetSize=maxSize_preview,
            format="webp",
            quality=previewQuality,
        )
        mediumBytes = resizeImageBytes(
            imageBytes=imageBytes,
            inverse=True,
            targetSize=maxSize_medium,
            format="webp",
            quality=80,
        )
    if resolution == "small":
        logger1.info("small")

        previewBytes = imageBytes = resizeImageBytes(
            imageBytes=imageBytes,
            format="webp",
            quality=previewQuality,
        )

        mediumBytes = imageBytes
        largeBytes = imageBytes

    return (resolution, previewBytes, mediumBytes, largeBytes)


def makeImgGivenLabColors(hexColors=None, w=200, h=50):
    nps = []
    w = w
    h = h
    for hexColorInfo in hexColors:
        hexColor, weight = hexColorInfo
        color = ImageColor.getcolor(hexColor, "RGB")
        w_ = int(w / 100 * weight)
        img = Image.new("RGB", (w_, h), color=color)
        nps.append(np.array(img))

    img_ = np.hstack(tuple(nps))
    return img_


def makeImgGivenLabColors(hexColors=None, w=200, h=50):
    nps = []
    w = w
    h = h
    for hexColorInfo in hexColors:
        hexColor, weight = hexColorInfo
        color = ImageColor.getcolor(hexColor, "RGB")
        w_ = int(w / 100 * weight)
        img = Image.new("RGB", (w_, h), color=color)
        nps.append(np.array(img))

    img_ = np.hstack(tuple(nps))
    return img_


def rgb2hex(rgb_number):
    """
    Args:
        - rgb_number (sequence of float)

    Returns:
        - hex_number (string)
    """
    return "#%02x%02x%02x" % tuple([int(np.round(val * 255)) for val in rgb_number])


def hex2rgb(hexcolor_str):
    """
    Args:
        - hexcolor_str (string): e.g. '#ffffff' or '33cc00'

    Returns:
        - rgb_color (sequence of floats): e.g. (0.2, 0.3, 0)
    """
    color = hexcolor_str.strip("#")
    rgb = lambda x: round(int(x, 16) / 255.0, 5)
    return (rgb(color[:2]), rgb(color[2:4]), rgb(color[4:6]))


def rgba2rgb(rgba, background=(255, 255, 255)):
    row, col, ch = rgba.shape

    if ch == 3:
        return rgba

    assert ch == 4, "RGBA image has 4 channels."

    rgb = np.zeros((row, col, 3), dtype="float32")
    r, g, b, a = rgba[:, :, 0], rgba[:, :, 1], rgba[:, :, 2], rgba[:, :, 3]

    a = np.asarray(a, dtype="float32") / 255.0

    R, G, B = background

    rgb[:, :, 0] = r * a + (1.0 - a) * R
    rgb[:, :, 1] = g * a + (1.0 - a) * G
    rgb[:, :, 2] = b * a + (1.0 - a) * B

    return np.asarray(rgb, dtype="uint8")


def rgba2Npys(imageNpy=None):
    r_channel = imageNpy[:, :, 0]
    g_channel = imageNpy[:, :, 1]
    b_channel = imageNpy[:, :, 2]
    imageNpy_ = np.zeros((imageNpy.shape[0], imageNpy.shape[1], 3), dtype=np.int8)
    imageNpy_[:, :, 0] = r_channel
    imageNpy_[:, :, 1] = g_channel
    imageNpy_[:, :, 2] = b_channel
    imageNpy_ = imageNpy_.astype(np.uint8)
    alpha_channel = imageNpy[:, :, 3]
    alphaNpy = np.squeeze(np.stack((alpha_channel,) * 3, axis=-1))
    return (imageNpy_, alphaNpy)


def imageBytes2ImageNpy(imageBytes=None, ifRgb=True):
    """
    mode: rgb, rgba
    如果imageBytes对应的是rgba的话,要想生成png,就必须保留,不能转成rgb,如果转成rgb, alpha channel will lost
    """
    img = pil_image.open(io.BytesIO(imageBytes))
    if ifRgb:
        if img.mode != "RGB":
            img = img.convert("RGB")

    img = np.array(img)
    return img


def imageNpy2ImageBytes(imageNpy=None, format="JPEG"):
    """
    如果npy是四位的对应rgba,format 必须设置成png才能最后生成png with alpha channel
    """
    img = pil_image.fromarray(imageNpy)
    newImageBytes = io.BytesIO()
    img.save(newImageBytes, format=format, quality=85)
    newImageBytes = newImageBytes.getvalue()
    return newImageBytes


def createWatermark(imageBytes=None, watermarkImageBytes=None):
    main = pil_image.open(io.BytesIO(imageBytes))
    mark = pil_image.open(io.BytesIO(watermarkImageBytes))
    # mark = mark.rotate(30, expand=1)
    mask = mark.convert("L").point(lambda x: min(x, 50))
    mark.putalpha(mask)
    mark_width, mark_height = mark.size
    main_width, main_height = main.size
    aspect_ratio = mark_width / mark_height
    new_mark_width = main_width * 0.3
    mark.thumbnail((new_mark_width, new_mark_width / aspect_ratio), Image.ANTIALIAS)
    mark_width, mark_height = mark.size

    # tmp_img = Image.new("RGBA", main.size)
    # for i in range(0, tmp_img.size[0], mark.size[0]):
    #     for j in range(0, tmp_img.size[1], mark.size[1]):
    #         main.paste(mark, (i, j), mark)
    x = int((main_width - mark_width) / 2)
    y = int((main_height - mark_height) / 2)
    logger1.info("x: %s, y: %s", x, y)
    main.paste(
        mark,
        (x, y),
        mark,
    )

    main.thumbnail(main.size, Image.ANTIALIAS)
    newImageBytes = io.BytesIO()
    main.save(newImageBytes, format="WEBP", quality=85)
    return newImageBytes.getvalue()
