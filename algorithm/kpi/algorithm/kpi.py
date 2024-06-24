import numpy as np

from algorithm import correlation
from algorithm.smooth import exponential_moving_average, simple_moving_average, weighted_moving_average
from graphic import draw
from parser.parse import DataParser


class Solution:
    def _calculate_returns(self, series):
        """
        计算时间序列的涨跌幅度（百分比变化）
        :param series: 时间序列
        :return: 涨跌幅度序列
        """
        series = np.array(series)
        return np.diff(series)

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
        :return: 输出前N个相关的KPI索引（从1开始）
        """
        # # 计算异常KPI的涨跌幅度
        # abnormal_kpi = self._calculate_returns(abnormal_kpi)
        #
        # # 计算所有KPI的涨跌幅度
        # kpis = [self._calculate_returns(kpi) for kpi in kpis]

        # 存储相关性值和对应的KPI索引
        correlation_scores = []

        # 计算每个观测KPI与异常KPI涨跌幅度之间的相关性
        for idx, kpi in enumerate(kpis):
            # correlation = self._safe_corrcoef(abnormal_kpi_returns, kpi)
            corr = correlation.distance_correlation(abnormal_kpi, kpi)
            correlation_scores.append((corr, idx + 1))  # 索引从1开始

        # 按相关性从高到低排序
        correlation_scores.sort(reverse=True, key=lambda x: x[0])

        # 提取前N个相关性最强的KPI索引
        top_n_indices = [idx for _, idx in correlation_scores[:top_n]]

        return top_n_indices


parser = DataParser('../data/kpi_test_data.txt')
parser.parse_data()
abnormal_kpi, kpis = parser.get_kpi_data()[1]

abnormal_kpi, kpis = simple_moving_average(abnormal_kpi, kpis)

solution = Solution()
result = solution.correlation_analysis(abnormal_kpi, kpis, 3)
print(result)
print([80, 58, 2])
