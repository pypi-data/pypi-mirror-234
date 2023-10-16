import numpy as np
from sklearn import preprocessing


def nns(queryFeatures, baseFeatures):
    # given query features npy, return theirs centerId based on self.centroids
    matchedCenterIds = []
    c = l2MatrixEdm(queryFeatures, baseFeatures)
    sortIndex = np.argsort(c, axis=1)[:, :5]

    for index, indexes in enumerate(sortIndex):
        matchIndex = indexes[0]

        matchedCenterIds.append(matchIndex)
    return matchedCenterIds


def l2MatrixEdm(A, B):
    """
    inputs must be l2NormAndRound, others nan error
    :param A:
    :param B:
    :return:
    """
    # p1=np.sum(A**2,axis=1)[:,np.newaxis]
    # p2 = np.sum(B ** 2, axis=1)
    p3 = -2 * np.dot(A, B.T)
    return np.round(np.sqrt(2 + p3), 2)


def l2NormAndRound(featureArray=None, norm="l2"):
    """

    :param features:  rank 2
    :return:
    supported norm:
    l1,l2,hellinger
    """
    assert norm in ["l1", "l2", "hellinger", None]
    eps = 1e-7
    if norm is not None:
        if norm == "hellinger":
            # featureArray = preprocessing.normalize(featureArray, norm='l2')
            # featureArray = preprocessing.normalize(featureArray, norm='l1')
            # featureArray = np.sqrt(featureArray)
            featureArray /= featureArray.sum(axis=1, keepdims=True) + eps
            featureArray = np.sqrt(featureArray)
        else:
            featureArray = preprocessing.normalize(featureArray, norm=norm)

    featureArray = np.around(featureArray, 3)
    return featureArray
