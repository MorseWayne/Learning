import numpy as np
import pandas as pd


def exponential_moving_average(abnormal_kpi, kpis):
    span_len = 20
    # 将abnormal_kpi数组转换为Pandas Series对象，然后使用指数加权移动平均进行平滑
    abnormal_kpi_series = pd.Series(abnormal_kpi)
    smoothed_abnormal_kpi = abnormal_kpi_series.ewm(span=span_len).mean()

    # 修正：对kpis列表中的每个kpi进行迭代，将其转换为Pandas Series，然后使用指数加权移动平均进行平滑
    smoothed_kpis = [pd.Series(kpi).ewm(span=span_len).mean() for kpi in kpis]

    # 如果需要的话，可以在这里将Pandas Series转换为numpy数组
    smoothed_abnormal_kpi_array = smoothed_abnormal_kpi.to_numpy()
    smoothed_kpis_arrays = [kpi_smoothed.to_numpy() for kpi_smoothed in smoothed_kpis]

    return smoothed_abnormal_kpi_array, smoothed_kpis_arrays


def simple_moving_average(abnormal_kpi, kpis):
    span_len = 20
    # 使用min_periods=1来避免NaN值
    abnormal_kpi_series = pd.Series(abnormal_kpi)
    smoothed_abnormal_kpi = abnormal_kpi_series.rolling(window=span_len, min_periods=1).mean()

    # 对kpis列表中的每个kpi进行迭代，将其转换为Pandas Series，然后使用简单移动平均进行平滑
    smoothed_kpis = [pd.Series(kpi).rolling(window=span_len, min_periods=1).mean() for kpi in kpis]

    # 转换为numpy数组
    smoothed_abnormal_kpi_array = smoothed_abnormal_kpi.to_numpy()
    smoothed_kpis_arrays = [kpi_smoothed.to_numpy() for kpi_smoothed in smoothed_kpis]

    return smoothed_abnormal_kpi_array, smoothed_kpis_arrays


def weighted_moving_average(abnormal_kpi, kpis, window_size=25):
    # 生成权重序列，权重随着接近当前时间而增加
    weights = np.arange(1, window_size + 1)

    # 对abnormal_kpi使用加权移动平均，因为pandas没有直接支持加权移动平均，所以使用numpy手动计算
    abnormal_kpi_series = pd.Series(abnormal_kpi)
    smoothed_abnormal_kpi = abnormal_kpi_series.rolling(window=window_size).apply(
        lambda x: np.dot(x, weights) / weights.sum(), raw=True)

    # 对kpis的每个元素应用加权移动平均
    smoothed_kpis = []
    for kpi in kpis:
        kpi_series = pd.Series(kpi)
        smoothed_kpis.append(
            kpi_series.rolling(window=window_size).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True))

    # 转换为numpy数组
    smoothed_abnormal_kpi_array = smoothed_abnormal_kpi.to_numpy()
    smoothed_kpis_arrays = [kpi_smoothed.to_numpy() for kpi_smoothed in smoothed_kpis]

    return smoothed_abnormal_kpi_array, smoothed_kpis_arrays
