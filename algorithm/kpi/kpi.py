import numpy as np


def simple_moving_average(data, window_size):
    """计算简单移动平均值

    Args:
        data: 数据列表
        window_size: 窗口大小

    Returns:
        平滑后的数据列表
    """
    sma = []
    for i in range(window_size, len(data) + 1):
        sma.append(np.mean(data[i - window_size:i]))
    return sma


def find_dominant_cycle(data):
    """
    使用傅里叶变换分析CPU使用率数据的周期性波动
    :param cpu_usage: CPU使用率的时间序列数据，列表或numpy数组
    :return: 如果存在周期性波动，则返回主要波动周期；否则返回0
    """
    # 傅里叶变换
    cpu_frequency = np.fft.fft(data)
    # 获取频率的幅度
    magnitudes = np.abs(cpu_frequency)
    # 忽略直流分量（第一个元素）并找到主频率的索引
    dominant_index = np.argmax(magnitudes[1:]) + 1
    # 计算样本点数量
    num_samples = len(data)
    # 计算主振幅对应的频率
    dominant_freq = dominant_index / num_samples
    # 如果主频率为0，说明没有周期性波动
    if dominant_freq == 0:
        return 0
    # 计算周期（秒），考虑样本点对应的实际时间跨度
    # 这里假设cpu_usage数组的每个元素间隔为1秒
    dominant_cycle = 1 / dominant_freq

    return dominant_cycle


class Solution:
    def _calculate_returns(self, series):
        """
        计算时间序列的涨跌幅度（百分比变化）
        :param series: 时间序列
        :return: 涨跌幅度序列
        """
        series = np.array(series)
        base_value = np.mean(series)
        if base_value == 0:
            base_value = 1

        return np.diff(series) / base_value

    def _safe_corrcoef(self, x, y):
        """
        安全计算相关性，处理标准差为零的情况
        :param x: 序列x
        :param y: 序列y
        :return: 相关性值
        """
        if np.std(x) == 0 or np.std(y) == 0:
            return 0  # 如果任一序列的标准差为零，则相关性定义为0
        return np.corrcoef(x, y)[0, 1]

    def correlation_analysis(self, abnormal_kpi, kpis, top_n):
        """
        KPI相关性分析
        -------------------------------------------------------------------
        :param abnormal_kpi: 存在异常波动的KPI
        :param kpis: 观测的一组KPI列表
        :param top_n: abnormal_kpi
        :param correlation_method: 相关性计算方法 ('pearson' 或 'spearman')
        :return: 输出前N个相关的KPI索引（从1开始）
        """
        # 计算异常KPI的涨跌幅度
        # window_size = round(len(abnormal_kpi) / 5) * 4
        # abnormal_kpi = simple_moving_average(abnormal_kpi, window_size)
        # kpis = [simple_moving_average(kpi, window_size) for kpi in kpis]

        cycle = round(find_dominant_cycle(abnormal_kpi))
        if cycle != 0:
            abnormal_kpi = abnormal_kpi[0:cycle]
            kpis = [kpi[0:cycle] for kpi in kpis]

        abnormal_kpi_returns = self._calculate_returns(abnormal_kpi)

        # 存储相关性值和对应的KPI索引
        correlation_scores = []

        # 计算所有KPI的涨跌幅度
        kpis_returns = [self._calculate_returns(kpi) for kpi in kpis]

        # 计算每个观测KPI与异常KPI涨跌幅度之间的相关性
        for idx, scaled_kpi in enumerate(kpis_returns):
            correlation = self._safe_corrcoef(abnormal_kpi_returns, scaled_kpi)
            correlation_scores.append((correlation, idx + 1))  # 索引从1开始

        # 按相关性从高到低排序
        correlation_scores.sort(reverse=True, key=lambda x: x[0])

        # 提取前N个相关性最强的KPI索引
        top_n_indices = [idx for _, idx in correlation_scores[:top_n]]

        return top_n_indices


# 示例用法
sol = Solution()
abnormal_kpi = [2, 6, 2, 4, 6]
kpis = [[3, 8, 3, 3, 8], [4, 12, 4, 8, 16], [0, 20, 8, 16, 16]]
top_n = 3
print(sol.correlation_analysis(abnormal_kpi, kpis, top_n))  # 输出示例: [1, 3, 2]
