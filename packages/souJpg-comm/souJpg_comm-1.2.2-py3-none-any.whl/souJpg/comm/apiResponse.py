from enum import Enum
from typing import Optional

from pydantic import BaseModel


class BaseResponse(BaseModel):
    error: Optional[str] = None
    errorCode: Optional[str] = None

    # async request related
    asyncRequestId: Optional[str] = None
    status: Optional[int] = None
    
    # 请求参数
    params: Optional[dict] = None
    
    
    # 
    
    
    leftQuota: Optional[int] = None
    
    
    


class ErrorCodeType(Enum):

    userRegisterError01 = "userRegisterError01"
    userRegisterError02 = "userRegisterError02"
    userLoginError01 = "userLoginError01"
    userLoginError02 = "userLoginError02"
    userLoginError03 = "userLoginError03"
    userUpdatedPasswordError01 = "userUpdatedPasswordError01"

    userAccountAbnormalException = "userAccountAbnormalException"

    userAuthError01 = "userAuthError01"
    permissionCheckError01 = "permissionCheckError01"
    permissionCheckError02 = "permissionCheckError02"
    permissionCheckError03 = "permissionCheckError03"

    # serviceName or serviceMethod not existed
    serviceNotExistedError01 = "serviceNotExistedError01"

    asyncRequestIdNotExist = "asyncRequestIdNotExist"

    userIdNotExist = "userIdNotExist"
    userIdMissing = "userIdMissing"
    tokenMissing = "tokenMissing"
    tokenInvalid = "tokenInvalid"

    modelInferServerBusy = "modelInferServerBusy"

    # login
    loginTypeNull = "loginTypeNull"
    loginTypeNotSupported = "loginTypeNotSupported"
    verifiedCodeNull = "verifiedCodeNull"
    verifiedCodeNotMatch = "verifiedCodeNotMatch"
    wxLoginCallbackError01 = "wxLoginCallbackError01"
    wxLoginCallbackError02 = "wxLoginCallbackError02"

    mobileNumberFormatError = "mobileNumberFormatError"

    # unknown error
    serverBusyError = "serverBusyError"

    resultImageUploadError = "resultImageUploadError"

    modelIdNotExist = "modelIdNotExist"

    modelIdNotNone = "modelIdNotNone"

    modelInferError = "modelInferError"

    # userGallery
    uploadImageToGalleryError01 = "uploadImageToGalleryError01"
    uploadImageToGalleryError02 = "uploadImageToGalleryError02"

    servicePlanKeyNotExist = "servicePlanKeyNotExist"
    InvalidServicePlanKeyPrice = "InvalidServicePlanKeyPrice"
    orderNotExist = "orderNotExist"
    orderNotPaid = "orderNotPaid"

    invoiceNotExist = "invoiceNotExist"
    invoiceUpdatedError = "invoiceUpdatedError"

    taskTypeIsNone = "taskTypeIsNone"
    taskParamsError = "taskParamsError"

    taskIdError = "taskIdError"
    taskNotFinished = "taskNotFinished"
    taskEmpty = "taskEmpty"
    taskResultSaveError = "taskResultSaveError"

    opNameNotExist = "opNameNotExist"

    alreadyBlinded = "alreadyBlinded"

    searchModeError = "searchModeError"
    
    unSupportImageFormat = "unSupportImageFormat"
