import matplotlib.pyplot as plt
import numpy as np
from parser import parse


def draw_fft_freq(data):
    data = np.array(data)
    # data[data < 90] = 99.5

    # 1. 进行离散傅里叶变换
    fft_result = np.fft.fft(data)
    num_samples = len(data)
    freq_vals = np.fft.fftfreq(num_samples, 1.0)

    plt.subplot(2, 1, 1)
    plt.plot(data)
    plt.title('CPU Usage Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('CPU Usage')

    # 绘制频域图像
    plt.subplot(2, 1, 2)
    plt.plot(np.arange(0, num_samples, 1), np.abs(freq_vals))
    plt.title('Frequency Domain')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.show()


def draw(datas):
    for i, data in enumerate(datas):
        time_index = [j + 1 for j in range(len(data))]
        plt.subplot(len(datas), 1, i + 1)
        data = np.array(data)
        plt.plot(time_index, data)
    plt.xlabel('Time (s)')
    plt.ylabel('value')
    plt.show()


class DataVisualizer:
    def __init__(self, data_parser):
        self.data_parser = data_parser

    def plot_kpi(self, index):
        """
        绘制指定索引的KPI数据
        :param index: 要绘制的KPI数据索引
        """
        kpi_data = self.data_parser.get_kpi_data()
        abnormal, kpi_values = kpi_data[index]

        windows_size = 13

        abnormal = parse.simple_moving_average(abnormal, windows_size)

        abnormal_len = len(abnormal)
        time_index = [i + 1 for i in range(abnormal_len)]

        num_kpis = len(kpi_values)
        fig, axes = plt.subplots(num_kpis + 1, 1, figsize=(10, 2 * num_kpis), sharex=True)
        fig.suptitle(f"KPI {index}")

        # 绘制abnormal数据
        ax_abnormal = axes[0]
        ax_abnormal.plot(time_index, abnormal, label='Abnormal Data', color='red')
        ax_abnormal.set_ylabel('Abnormal')
        ax_abnormal.grid(True)
        ax_abnormal.legend()

        fig.canvas.toolbar_visible = False

        # 绘制每个KPI数据
        for i, kpi in enumerate(kpi_values):
            kpi = parse.simple_moving_average(kpi, windows_size)
            ax = axes[i + 1]
            ax.plot(time_index, kpi, label=f'KPI {i + 1} Data')
            # ax.set_ylabel(f'KPI {i + 1}')
            ax.grid(True)
            ax.legend()

        # plt.xticks(time_index)
        plt.xlabel("Time")
        plt.show()

# parser = parse.DataParser('kpi_test_data.txt')
# parser.parse_data()
#
# visualizer = DataVisualizer(parser)
# visualizer.plot_kpi(1)  # 绘制第一个KPI数据
