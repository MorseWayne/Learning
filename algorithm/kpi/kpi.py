# 运维过程中需要监控很多性能指标（后面统一称为KPI），
# 进而感知网络的质量状态。KPI之间可能存在一定的相关性（具体指波动相关，KPI波动的定义可参考CoFlux算法），
# 如KPI1值升高可能引发KPI2值下降、KPI3值升高等。为了辅助运维人员对异常的KPI进行根因诊断，
# 期望能够仅根据异常KPI及其他监控的KPI的时间序列，找出与异常KPI相关性最强的KPI，并进行TopN排序。
# 选手需要根据输入的异常KPI时间序列及一组观测的其他KPI时间序列（均无标记，KPI序列的时间粒度及长度都是一致的），
# 设计合适的相关性算法，实现KPI的相关性排序，从而确定导致KPI异常的根因。
# 输入
# 1、参数1：异常KPI时间序列
# 2、参数2：其余观测KPI的时间序列
# 3、参数3：需要输出与异常KPI最相关的其余观测KPI个数
# 注：KPI数量<=200, 时间序列长度 <=2000；所有KPI时间序列的长度一致
#
# 输出
# 按相关性由强到弱排序输出TopN相关性KPI的索引(从1开始)
#
# 样例
# 输入样例 1
# [2,6,2,4,6], [[3,8,3,3,8], [4,12,4,8,16], [0,20,8,16,16]],3
#
# 输出样例 1
# [1, 3, 2]
#

import numpy as np
from scipy.stats import spearmanr

class Solution:

    def _calculate_fluctuations(self, series, window_size=1):
        """
        计算时间序列的波动部分（滑动窗口差分）
        :param series: 时间序列
        :param window_size: 滑动窗口大小
        :return: 波动部分的序列
        """
        if window_size == 1:
            return np.diff(series)
        else:
            return series[window_size:] - series[:-window_size]

    def correlation_analysis(self, abnormal_kpi, kpis, top_n, correlation_method='pearson', window_size=1):
        """
        KPI相关性分析
        -------------------------------------------------------------------
        :param abnormal_kpi: 存在异常波动的KPI
        :param kpis: 观测的一组KPI列表
        :param top_n: 输出相关KPI的个数
        :param correlation_method: 相关性计算方法 ('pearson' 或 'spearman')
        :param window_size: 滑动窗口大小
        :return: 输出前N个相关的KPI索引（从1开始）
        """
        # 将异常KPI转换为NumPy数组并计算波动部分
        abnormal_kpi_fluctuations = self._calculate_fluctuations(np.array(abnormal_kpi), window_size)

        # 存储相关性值和对应的KPI索引
        correlation_scores = []

        # 将所有KPI转换为NumPy数组并计算波动部分
        kpis_fluctuations = [self._calculate_fluctuations(np.array(kpi), window_size) for kpi in kpis]

        # 计算每个观测KPI与异常KPI的波动部分之间的相关性
        for idx, kpi_fluctuations in enumerate(kpis_fluctuations):
            if correlation_method == 'pearson':
                correlation = np.corrcoef(abnormal_kpi_fluctuations, kpi_fluctuations)[0, 1]
            elif correlation_method == 'spearman':
                correlation, _ = spearmanr(abnormal_kpi_fluctuations, kpi_fluctuations)
            else:
                raise ValueError("Unsupported correlation method. Use 'pearson' or 'spearman'.")
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
print(sol.correlation_analysis(abnormal_kpi, kpis, top_n, correlation_method='spearman', window_size=1))  # 输出示例: [1, 3, 2]
