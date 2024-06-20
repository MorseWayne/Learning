import matplotlib.pyplot as plt
from parse import DataParser


class DataVisualizer:
    def __init__(self, data_parser):
        self.data_parser = data_parser

    def plot_kpi(self, index):
        """
        绘制指定索引的KPI数据
        :param index: 要绘制的KPI数据索引
        """
        abnormal, kpi_values = self.data_parser.get_kpi_data()[index]

        # kpi_values = kpi_values[0:10]

        abnormal_len = len(abnormal)
        time_index = [i + 1 for i in range(abnormal_len)]

        num_kpis = len(kpi_values)
        fig, axes = plt.subplots(num_kpis + 1, 1, figsize=(10, 2 * num_kpis), sharex=True)
        fig.suptitle(f"KPI {index + 1}")

        # 绘制abnormal数据
        ax_abnormal = axes[0]
        ax_abnormal.plot(time_index, abnormal, label='Abnormal Data', color='red')
        ax_abnormal.set_ylabel('Abnormal')
        ax_abnormal.grid(True)
        ax_abnormal.legend()

        fig.canvas.toolbar_visible = False

        # 绘制每个KPI数据
        for i, kpi in enumerate(kpi_values):
            ax = axes[i + 1]
            ax.plot(time_index, kpi, label=f'KPI {i + 1} Data')
            # ax.set_ylabel(f'KPI {i + 1}')
            ax.grid(True)
            ax.legend()

        plt.xlabel("Time")
        plt.show()


# 使用示例
parser = DataParser('kpi_test_data.txt')
parser.parse_data()

visualizer = DataVisualizer(parser)
visualizer.plot_kpi(0)  # 绘制第一个KPI数据
