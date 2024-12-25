import sys
from collections import OrderedDict
from datetime import datetime

import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Patch

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QMessageBox
)

# 设置中文显示及负号
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False


class HourlyAirQualityForecast(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("逐小时空气质量预报")
        self.setFixedSize(1200, 800)

        self.data = []               # 保存逐小时空气质量预报数据
        self.current_chart = 0       # 当前显示的图表索引
        self.chart_titles = [
            "空气质量指数 (AQI)",
            "PM2.5", "PM10", "SO2", "NO2", "CO", "O3"
        ]

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入框：城市名称
        self.input_city = QLineEdit()
        self.input_city.setPlaceholderText("请输入城市名称，例如: 北京")
        layout.addWidget(self.input_city)

        # 获取空气质量预报按钮
        btn_fetch = QPushButton("获取逐小时空气质量预报")
        btn_fetch.clicked.connect(self.fetch_hourly_air_quality)
        layout.addWidget(btn_fetch)

        # Matplotlib 图表区域
        self.canvas = FigureCanvas(Figure(figsize=(18, 6)))  # 图表区域尺寸调大，避免拥挤
        layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.add_subplot(111)

        # 切换图表按钮
        button_layout = QHBoxLayout()
        self.prev_button = QPushButton("上一图表")
        self.prev_button.clicked.connect(self.show_previous_chart)
        self.prev_button.setEnabled(False)
        button_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("下一图表")
        self.next_button.clicked.connect(self.show_next_chart)
        self.next_button.setEnabled(False)
        button_layout.addWidget(self.next_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def fetch_hourly_air_quality(self):
        city = self.input_city.text().strip()

        if not city:
            QMessageBox.warning(self, "警告", "城市名称不能为空！")
            return

        try:
            air_data = self.api_client.fetch_hourly_air_quality_forecast(location=city)
            self.data = air_data.get('results', [{}])[0].get('hourly', [])
            if not self.data:
                QMessageBox.information(self, "提示", "当前城市暂无空气质量预报数据！")
                return

            # 去重并按时间排序
            self.data = list(OrderedDict((hour['time'], hour) for hour in self.data).values())

            self.current_chart = 0
            self.update_chart()
            self.prev_button.setEnabled(True)
            self.next_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取空气质量预报数据失败: {e}")

    def update_chart(self):
        if not self.data:
            return

        # 清空图表
        self.ax.clear()

        # 格式化时间为 日-小时 (如 "25-19" 表示 25号19点)
        times = [
            datetime.strptime(hour['time'], "%Y-%m-%dT%H:%M:%S%z").strftime("%d-%H")
            for hour in self.data
        ]

        # 提取各项数据
        data_map = {
            0: [int(hour['aqi']) for hour in self.data],    # AQI
            1: [float(hour['pm25']) for hour in self.data], # PM2.5
            2: [float(hour['pm10']) for hour in self.data], # PM10
            3: [float(hour['so2']) for hour in self.data],  # SO2
            4: [float(hour['no2']) for hour in self.data],  # NO2
            5: [float(hour['co']) for hour in self.data],   # CO
            6: [float(hour['o3']) for hour in self.data],   # O3
        }

        y_data = data_map[self.current_chart]
        title = self.chart_titles[self.current_chart]
        ylabel = title.split()[0]  # "空气质量指数" or "PM2.5" etc.

        # 绘制折线图
        self.ax.plot(range(len(times)), y_data, marker='o', label=title, color='blue')
        self.ax.set_title(title)
        self.ax.set_xlabel("时间 (日-小时)")
        self.ax.set_ylabel(f"{ylabel} 浓度")
        # 设置 X 轴刻度点 (均匀减少显示)
        self.ax.set_xticks(range(0, len(times), max(1, len(times) // 10)))
        self.ax.set_xticklabels(times[::max(1, len(times) // 10)], rotation=45, ha='right')
        self.ax.grid(True)

        # 如果当前图表是 AQI，则使用颜色分层 + 动态设置范围 + 图例
        if self.current_chart == 0:

            max_aqi = max(y_data) if y_data else 0

            #    intervals[i] ~ intervals[i+1] 的颜色为 colors[i]
            intervals = [0, 50, 100, 150, 200, 300]
            colors = ["green", "yellow", "orange", "red", "purple", "brown"]

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

            self.ax.set_ylim(0, y_upper)

            # 动态填充背景色: 只到 y_upper
            for i in range(len(intervals) - 1):
                low = intervals[i]
                high = intervals[i + 1]
                if high > y_upper:
                    self.ax.axhspan(low, y_upper, facecolor=colors[i], alpha=0.15)
                    break  # 超过 y_upper 后，就不用再画后面区间了
                else:
                    self.ax.axhspan(low, high, facecolor=colors[i], alpha=0.15)

            # 如果 max_aqi > 300，需要再单独填充 300~y_upper 区间 (棕色)
            if max_aqi > 300:
                self.ax.axhspan(300, y_upper, facecolor="brown", alpha=0.15)

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
            # 若 >300 则 6 档都显示

            self.ax.legend(
                handles=patches,
                loc="upper left",
                title="污染等级",
                fancybox=True
            )

        self.canvas.draw()

    def show_previous_chart(self):
        if self.current_chart > 0:
            self.current_chart -= 1
            self.update_chart()

    def show_next_chart(self):
        if self.current_chart < len(self.chart_titles) - 1:
            self.current_chart += 1
            self.update_chart()

if __name__ == "__main__":
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为你的实际 API Key

    window = HourlyAirQualityForecast(api_client)
    window.show()
    sys.exit(app.exec())
