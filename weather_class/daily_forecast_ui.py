import sys

import matplotlib
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QPushButton, QLineEdit, QWidget, QMessageBox
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体以支持中文显示
matplotlib.rcParams['axes.unicode_minus'] = False  # 正确显示负号

class DailyForecast(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("逐日天气预报")
        self.setFixedSize(800, 800)

        self.data = []  # 保存逐日天气数据

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入框：城市名称
        self.input_city = QLineEdit()
        self.input_city.setPlaceholderText("请输入城市名称，例如: 北京")
        layout.addWidget(self.input_city)

        # 输入框：天数
        self.input_days = QLineEdit()
        self.input_days.setPlaceholderText("请输入天数，最多15天")
        layout.addWidget(self.input_days)

        # 获取天气按钮
        btn_fetch = QPushButton("获取逐日天气预报")
        btn_fetch.clicked.connect(self.fetch_daily_forecast)
        layout.addWidget(btn_fetch)

        # 显示天气信息
        self.weather_info = QLabel("点击按钮获取逐日天气预报")
        self.weather_info.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.weather_info)

        self.setLayout(layout)

        # Matplotlib 图表区域
        self.canvas = FigureCanvas(Figure(figsize=(10, 8)))
        layout.addWidget(self.canvas)
        self.ax_high = self.canvas.figure.add_subplot(511)
        self.ax_low = self.canvas.figure.add_subplot(512)
        self.ax_precip = self.canvas.figure.add_subplot(513)
        self.ax_wind = self.canvas.figure.add_subplot(514)
        self.ax_humidity = self.canvas.figure.add_subplot(515)
        self.canvas.figure.tight_layout(pad=5.0)

    def fetch_daily_forecast(self):
        city = self.input_city.text().strip()
        days = self.input_days.text().strip()

        if not city:
            QMessageBox.warning(self, "警告", "城市名称不能为空！")
            return

        if not days.isdigit() or int(days) < 1 or int(days) > 15:
            QMessageBox.warning(self, "警告", "请输入有效的天数（1~15）！")
            return

        try:
            weather_data = self.api_client.fetch_daily_forecast(location=city, days=int(days))
            self.data = weather_data.get('results', [{}])[0].get('daily', [])
            if not self.data:
                QMessageBox.warning(self, "警告", "未获取到天气数据！")
                return

            self.plot_weather_data()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取天气数据失败: {e}")

    def plot_weather_data(self):
        if not self.data:
            return

        dates = [day['date'][5:] for day in self.data]  # 去掉年份，仅显示月-日
        highs = [int(day['high']) for day in self.data]
        lows = [int(day['low']) for day in self.data]
        precips = [float(day['precip']) for day in self.data]
        wind_speeds = [float(day['wind_speed']) for day in self.data]
        wind_directions = [day['wind_direction'] for day in self.data]
        humidities = [float(day['humidity']) for day in self.data]
        day_texts = [day['text_day'] for day in self.data]
        night_texts = [day['text_night'] for day in self.data]

        self.ax_high.clear()
        self.ax_low.clear()
        self.ax_precip.clear()
        self.ax_wind.clear()
        self.ax_humidity.clear()

        # 最高温度
        self.ax_high.plot(dates, highs, marker='o', label="最高温度")
        self.ax_high.set_title("最高温度")
        self.ax_high.set_xlabel("日期")
        self.ax_high.set_ylabel("温度 (°C)")
        self.ax_high.grid(True)

        # 最低温度
        self.ax_low.plot(dates, lows, marker='o', label="最低温度", color='blue')
        self.ax_low.set_title("最低温度")
        self.ax_low.set_xlabel("日期")
        self.ax_low.set_ylabel("温度 (°C)")
        self.ax_low.grid(True)

        # 降水概率
        self.ax_precip.plot(dates, precips, marker='o', label="降水概率", color='green')
        self.ax_precip.set_title("降水概率")
        self.ax_precip.set_xlabel("日期")
        self.ax_precip.set_ylabel("概率 (%)")
        self.ax_precip.grid(True)

        # 风速
        self.ax_wind.plot(dates, wind_speeds, marker='o', label="风速", color='orange')
        for i, direction in enumerate(wind_directions):
            self.ax_wind.annotate(direction, (dates[i], wind_speeds[i]), textcoords="offset points", xytext=(0, 10), ha='center')
        self.ax_wind.set_title("风速")
        self.ax_wind.set_xlabel("日期")
        self.ax_wind.set_ylabel("风速 (km/h)")
        self.ax_wind.grid(True)

        # 湿度
        self.ax_humidity.plot(dates, humidities, marker='o', label="湿度", color='purple')
        self.ax_humidity.set_title("湿度")
        self.ax_humidity.set_xlabel("日期")
        self.ax_humidity.set_ylabel("湿度 (%)")
        self.ax_humidity.grid(True)

        self.canvas.draw()

        # 更新白天天气和晚间天气
        self.weather_info.setText(f"白天天气: {day_texts[0]}\n晚间天气: {night_texts[0]}")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key
    window = DailyForecast(api_client)
    window.show()
    sys.exit(app.exec())
