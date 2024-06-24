from scipy.spatial import distance
import numpy as np


# 定义计算距离相关系数的函数
def distance_correlation(X, Y):
    n = len(X)
    if n != len(Y):
        raise ValueError("X and Y must have the same length.")

    # 计算距离矩阵
    A = distance.squareform(distance.pdist(X[:, None]))
    B = distance.squareform(distance.pdist(Y[:, None]))

    # 计算均值距离矩阵
    A_mean = A.mean()
    B_mean = B.mean()

    # 计算距离矩阵的均值中心化矩阵
    A_centered = A - A.mean(axis=0) - A.mean(axis=1)[:, None] + A_mean
    B_centered = B - B.mean(axis=0) - B.mean(axis=1)[:, None] + B_mean

    # 计算距离相关系数
    numerator = (A_centered * B_centered).sum()
    denominator = np.sqrt((A_centered ** 2).sum() * (B_centered ** 2).sum())
    if denominator == 0:
        return np.nan
    return numerator / denominator
