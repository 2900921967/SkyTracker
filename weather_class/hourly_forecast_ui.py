import sys

import matplotlib
from PyQt6.QtWidgets import (
    QVBoxLayout, QPushButton, QLineEdit, QWidget, QMessageBox
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

class HourlyForecast(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("24小时逐小时天气预报")
        self.setFixedSize(800, 800)

        self.data = []  # 保存逐小时天气数据

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入框：城市名称
        self.input_city = QLineEdit()
        self.input_city.setPlaceholderText("请输入城市名称，例如: 北京")
        layout.addWidget(self.input_city)

        # 输入框：小时数
        self.input_hours = QLineEdit()
        self.input_hours.setPlaceholderText("请输入小时数，最多24小时")
        layout.addWidget(self.input_hours)

        # 获取天气按钮
        btn_fetch = QPushButton("获取逐小时天气预报")
        btn_fetch.clicked.connect(self.fetch_hourly_forecast)
        layout.addWidget(btn_fetch)

        # Matplotlib 图表区域
        self.canvas = FigureCanvas(Figure(figsize=(10, 8)))
        layout.addWidget(self.canvas)
        self.ax_temperature = self.canvas.figure.add_subplot(311)
        self.ax_humidity = self.canvas.figure.add_subplot(312)
        self.ax_wind = self.canvas.figure.add_subplot(313)
        self.canvas.figure.tight_layout(pad=5.0)

        self.setLayout(layout)

    def fetch_hourly_forecast(self):
        city = self.input_city.text().strip()
        hours = self.input_hours.text().strip()

        if not city:
            QMessageBox.warning(self, "警告", "城市名称不能为空！")
            return

        if not hours.isdigit() or int(hours) < 1 or int(hours) > 24:
            QMessageBox.warning(self, "警告", "请输入有效的小时数（1~24）！")
            return

        try:
            weather_data = self.api_client.fetch_hourly_forecast(location=city, hours=int(hours))
            self.data = weather_data.get('results', [{}])[0].get('hourly', [])
            if not self.data:
                QMessageBox.warning(self, "警告", "未获取到天气数据！")
                return

            self.plot_weather_data()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取天气数据失败: {e}")

    def plot_weather_data(self):
        if not self.data:
            return

        # 修复小时提取问题
        hours = [hour['time'].split('T')[-1].split(':')[0] for hour in self.data]  # 提取小时部分
        temperatures = [float(hour['temperature']) for hour in self.data]
        humidities = [float(hour['humidity']) for hour in self.data]
        wind_speeds = [float(hour['wind_speed']) for hour in self.data]
        wind_directions = [hour['wind_direction'] for hour in self.data]
        weather_texts = [hour['text'] for hour in self.data]  # 获取天气描述

        self.ax_temperature.clear()
        self.ax_humidity.clear()
        self.ax_wind.clear()

        # 温度
        self.ax_temperature.plot(hours, temperatures, marker='o', label="温度")
        for i, text in enumerate(weather_texts):
            self.ax_temperature.annotate(text, (hours[i], temperatures[i]), textcoords="offset points", xytext=(0, 10), ha='center')
        self.ax_temperature.set_title("温度")
        self.ax_temperature.set_xlabel("时间 (小时)")
        self.ax_temperature.set_ylabel("温度 (°C)")
        self.ax_temperature.grid(True)

        # 湿度
        self.ax_humidity.plot(hours, humidities, marker='o', label="湿度", color='blue')
        self.ax_humidity.set_title("湿度")
        self.ax_humidity.set_xlabel("时间 (小时)")
        self.ax_humidity.set_ylabel("湿度 (%)")
        self.ax_humidity.grid(True)

        # 风速
        self.ax_wind.plot(hours, wind_speeds, marker='o', label="风速", color='orange')
        for i, direction in enumerate(wind_directions):
            self.ax_wind.annotate(direction, (hours[i], wind_speeds[i]), textcoords="offset points", xytext=(0, 10), ha='center')
        self.ax_wind.set_title("风速")
        self.ax_wind.set_xlabel("时间 (小时)")
        self.ax_wind.set_ylabel("风速 (km/h)")
        self.ax_wind.grid(True)

        self.canvas.draw()

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key
    window = HourlyForecast(api_client)
    window.show()
    sys.exit(app.exec())
