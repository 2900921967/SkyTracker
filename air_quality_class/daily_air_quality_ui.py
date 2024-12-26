import sys
from collections import OrderedDict
from datetime import datetime

import matplotlib
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit, QMessageBox
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Patch

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

class DailyAirQuality(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("逐日空气质量预报")
        self.setFixedSize(1200, 800)

        self.data = []  # 保存逐日空气质量预报数据

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入框：城市名称
        self.input_city = QLineEdit()
        self.input_city.setPlaceholderText("请输入城市名称，例如: 北京")
        layout.addWidget(self.input_city)

        # 获取空气质量预报按钮
        btn_fetch = QPushButton("获取逐日空气质量预报")
        btn_fetch.clicked.connect(self.fetch_daily_air_quality)
        layout.addWidget(btn_fetch)

        # Matplotlib 图表区域
        self.canvas = FigureCanvas(Figure(figsize=(15, 10)))  # 图表区域尺寸调大，避免拥挤
        layout.addWidget(self.canvas)

        # 创建多个子图（2 行 4 列布局）
        self.ax_aqi = self.canvas.figure.add_subplot(241)  # 空气质量指数 (AQI)
        self.ax_pm25 = self.canvas.figure.add_subplot(242)  # PM2.5
        self.ax_pm10 = self.canvas.figure.add_subplot(243)  # PM10
        self.ax_so2 = self.canvas.figure.add_subplot(244)  # SO2
        self.ax_no2 = self.canvas.figure.add_subplot(245)  # NO2
        self.ax_co = self.canvas.figure.add_subplot(246)   # CO
        self.ax_o3 = self.canvas.figure.add_subplot(247)   # O3

        self.canvas.figure.tight_layout(pad=5.0)  # 调整子图间距

        self.setLayout(layout)

    def fetch_daily_air_quality(self):
        city = self.input_city.text().strip()

        if not city:
            QMessageBox.warning(self, "警告", "城市名称不能为空！")
            return

        try:
            air_data = self.api_client.fetch_daily_air_quality(location=city)
            self.data = air_data.get('results', [{}])[0].get('daily', [])
            if not self.data:
                QMessageBox.information(self, "提示", "当前城市暂无空气质量预报数据！")
                return

            self.plot_air_quality_data()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取空气质量预报数据失败: {e}")

    def plot_air_quality_data(self):
        if not self.data:
            return

        # 去重并按日期排序
        unique_data = list(OrderedDict((day['date'], day) for day in self.data).values())

        # 格式化日期为 MM-DD
        dates = [day['date'] for day in unique_data]
        formatted_dates = [datetime.strptime(date, "%Y-%m-%d").strftime("%m-%d") for date in dates]

        # 提取各项数据
        aqi = [int(day['aqi']) for day in unique_data]
        pm25 = [float(day['pm25']) for day in unique_data]
        pm10 = [float(day['pm10']) for day in unique_data]
        so2 = [float(day['so2']) for day in unique_data]
        no2 = [float(day['no2']) for day in unique_data]
        co = [float(day['co']) for day in unique_data]
        o3 = [float(day['o3']) for day in unique_data]

        # 清空图表
        self.ax_aqi.clear()
        self.ax_pm25.clear()
        self.ax_pm10.clear()
        self.ax_so2.clear()
        self.ax_no2.clear()
        self.ax_co.clear()
        self.ax_o3.clear()

        # 绘制 AQI 折线图并分段背景着色
        self.plot_aqi_with_background(formatted_dates, aqi)

        # 设置所有图表的 x 轴标签
        for ax in [self.ax_aqi, self.ax_pm25, self.ax_pm10, self.ax_so2, self.ax_no2, self.ax_co, self.ax_o3]:
            ax.set_xticks(range(len(formatted_dates)))
            ax.set_xticklabels(formatted_dates, rotation=0)  # 水平显示标签

        # 绘制其他污染物折线图
        self.plot_generic_chart(self.ax_pm25, formatted_dates, pm25, "PM2.5", "浓度 (微克每立方米)", "blue")
        self.plot_generic_chart(self.ax_pm10, formatted_dates, pm10, "PM10", "浓度 (微克每立方米)", "orange")
        self.plot_generic_chart(self.ax_so2, formatted_dates, so2, "SO2", "浓度 (微克每立方米)", "green")
        self.plot_generic_chart(self.ax_no2, formatted_dates, no2, "NO2", "浓度 (微克每立方米)", "purple")
        self.plot_generic_chart(self.ax_co, formatted_dates, co, "CO", "浓度 (毫克每立方米)", "brown")
        self.plot_generic_chart(self.ax_o3, formatted_dates, o3, "O3", "浓度 (微克每立方米)", "red")

        # 刷新图表
        self.canvas.draw()

    def plot_generic_chart(self, ax, x_data, y_data, title, ylabel, color):
        """通用的绘图函数"""
        ax.plot(range(len(x_data)), y_data, marker='o', label=title, color=color)
        ax.set_title(title)
        ax.set_xlabel("日期")
        ax.set_ylabel(ylabel)
        ax.grid(True)

    def plot_aqi_with_background(self, dates, aqi):
        x_vals = range(len(dates))

        # 绘制折线图
        self.ax_aqi.plot(x_vals, aqi, marker='o', label="AQI", color='blue')
        self.ax_aqi.set_title("空气质量指数 (AQI)")
        self.ax_aqi.set_xlabel("日期")
        self.ax_aqi.set_ylabel("AQI")
        self.ax_aqi.grid(True)

        self.ax_aqi.set_xticks(x_vals)
        self.ax_aqi.set_xticklabels(dates, rotation=0)

        max_aqi = max(aqi) if aqi else 0

        # 依据最大 AQI 设置 y 轴上限
        if max_aqi <= 50:
            y_upper = 50
        elif max_aqi <= 100:
            y_upper = 100
        elif max_aqi <= 150:
            y_upper = 150
        elif max_aqi <= 200:
            y_upper = 200
        elif max_aqi <= 300:
            y_upper = 300
        else:
            y_upper = max_aqi + 10

        self.ax_aqi.set_ylim(0, y_upper)

        # 定义分段区间和对应的颜色
        intervals = [0, 50, 100, 150, 200, 300]
        colors = ["green", "yellow", "orange", "red", "purple", "brown"]

        # 依次填充背景颜色
        for i in range(len(intervals) - 1):
            low = intervals[i]
            high = intervals[i+1]

            if high > y_upper:
                # 若超过 y_upper，则只填充到 y_upper 即可
                self.ax_aqi.axhspan(low, y_upper, facecolor=colors[i], alpha=0.15)
                break
            else:
                self.ax_aqi.axhspan(low, high, facecolor=colors[i], alpha=0.15)

        # 如果 max_aqi > 300，需要再单独填充 300~y_upper 区间
        if max_aqi > 300:
            self.ax_aqi.axhspan(300, y_upper, facecolor="brown", alpha=0.15)

        # 为不同区间创建图例
        patches = [
            Patch(facecolor="green",  alpha=0.15, label="0-50：优"),
            Patch(facecolor="yellow", alpha=0.15, label="50-100：良"),
            Patch(facecolor="orange", alpha=0.15, label="100-150：轻度污染"),
            Patch(facecolor="red",    alpha=0.15, label="150-200：中度污染"),
            Patch(facecolor="purple", alpha=0.15, label="200-300：重度污染"),
            Patch(facecolor="brown",  alpha=0.15, label=">300：严重污染"),
        ]

        # 根据 max_aqi 决定要显示哪些档位
        if max_aqi <= 50:
            patches = patches[:1]
        elif max_aqi <= 100:
            patches = patches[:2]
        elif max_aqi <= 150:
            patches = patches[:3]
        elif max_aqi <= 200:
            patches = patches[:4]
        elif max_aqi <= 300:
            patches = patches[:5]
        # 如果大于 300，就 6 档都显示

        self.ax_aqi.legend(handles=patches, loc="lower left", title="污染等级", fancybox=True)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = DailyAirQuality(api_client)
    window.show()
    sys.exit(app.exec())
