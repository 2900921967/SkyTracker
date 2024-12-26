import sys

import matplotlib
from PyQt6.QtWidgets import (
    QVBoxLayout, QPushButton, QLineEdit, QWidget, QMessageBox
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

class HourlyHistory(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("过去24小时历史天气")
        self.setFixedSize(1650, 850)

        self.data = []  # 保存历史天气数据

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入框：城市名称
        self.input_city = QLineEdit()
        self.input_city.setPlaceholderText("请输入城市名称，例如: 北京")
        layout.addWidget(self.input_city)

        # 获取天气按钮
        btn_fetch = QPushButton("获取过去24小时历史天气")
        btn_fetch.clicked.connect(self.fetch_hourly_history)
        layout.addWidget(btn_fetch)

        # Matplotlib 图表区域
        self.canvas = FigureCanvas(Figure(figsize=(15, 10)))
        layout.addWidget(self.canvas)
        self.ax_temperature = self.canvas.figure.add_subplot(241)
        self.ax_pressure = self.canvas.figure.add_subplot(242)
        self.ax_humidity = self.canvas.figure.add_subplot(243)
        self.ax_visibility = self.canvas.figure.add_subplot(244)
        self.ax_wind_speed = self.canvas.figure.add_subplot(245)
        self.ax_clouds = self.canvas.figure.add_subplot(246)
        self.ax_dew_point = self.canvas.figure.add_subplot(247)
        self.canvas.figure.tight_layout(pad=5.0)

        self.setLayout(layout)

    def fetch_hourly_history(self):
        city = self.input_city.text().strip()

        if not city:
            QMessageBox.warning(self, "警告", "城市名称不能为空！")
            return

        try:
            weather_data = self.api_client.fetch_hourly_history(location=city)
            raw_data = weather_data.get('results', [{}])[0].get('hourly_history', [])

            # 去重逻辑，按小时去重
            seen_hours = set()
            unique_data = []
            for item in raw_data:
                hour = item['last_update'].split('T')[-1][:2]  # 提取小时部分
                if hour not in seen_hours:
                    seen_hours.add(hour)
                    unique_data.append(item)

            # 排序并移除最后一个数据点
            self.data = sorted(unique_data, key=lambda x: x['last_update'])
            if len(self.data) > 1:
                self.data.pop()

            if not self.data:
                QMessageBox.warning(self, "警告", "未获取到天气数据！")
                return

            self.plot_weather_data()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取天气数据失败: {e}")

    def plot_weather_data(self):
        if not self.data:
            return

        # 提取数据
        hourly_data = sorted(self.data, key=lambda x: x['last_update'])  # 确保按时间顺序排序
        times = [hour['last_update'].split('T')[-1][:2] for hour in hourly_data]  # 提取小时和分钟部分  # 提取小时部分
        temperatures = [float(hour['temperature']) for hour in hourly_data]
        feels_like = [float(hour['feels_like']) for hour in hourly_data]
        pressures = [float(hour['pressure']) for hour in hourly_data]
        humidities = [float(hour['humidity']) for hour in hourly_data]
        visibilities = [float(hour['visibility']) for hour in hourly_data]
        wind_speeds = [float(hour['wind_speed']) for hour in hourly_data]
        wind_directions = [hour['wind_direction'] for hour in hourly_data]
        clouds = [float(hour['clouds']) for hour in hourly_data]
        dew_points = [float(hour['dew_point']) if hour['dew_point'] else None for hour in hourly_data]
        weather_texts = [hour['text'] for hour in hourly_data]

        # 清空图表
        self.ax_temperature.clear()
        self.ax_pressure.clear()
        self.ax_humidity.clear()
        self.ax_visibility.clear()
        self.ax_wind_speed.clear()
        self.ax_clouds.clear()
        self.ax_dew_point.clear()

        # 温度与天气
        self.ax_temperature.plot(times, temperatures, marker='o', label="温度")
        self.ax_temperature.plot(times, feels_like, marker='o', label="体感温度", color='orange')
        for i, text in enumerate(weather_texts):
            self.ax_temperature.annotate(text, (times[i], temperatures[i]), textcoords="offset points", xytext=(0, 10), ha='center')
        self.ax_temperature.set_title("温度与体感温度")
        self.ax_temperature.set_xlabel("时间 (小时)")
        self.ax_temperature.set_ylabel("温度 (°C)")
        self.ax_temperature.legend()
        self.ax_temperature.grid(True)

        # 气压
        self.ax_pressure.plot(times, pressures, marker='o', label="气压", color='blue')
        self.ax_pressure.set_title("气压")
        self.ax_pressure.set_xlabel("时间 (小时)")
        self.ax_pressure.set_ylabel("气压 (mb)")
        self.ax_pressure.grid(True)

        # 湿度
        self.ax_humidity.plot(times, humidities, marker='o', label="湿度", color='green')
        self.ax_humidity.set_title("湿度")
        self.ax_humidity.set_xlabel("时间 (小时)")
        self.ax_humidity.set_ylabel("湿度 (%)")
        self.ax_humidity.grid(True)

        # 能见度
        self.ax_visibility.plot(times, visibilities, marker='o', label="能见度", color='purple')
        self.ax_visibility.set_title("能见度")
        self.ax_visibility.set_xlabel("时间 (小时)")
        self.ax_visibility.set_ylabel("能见度 (km)")
        self.ax_visibility.grid(True)

        # 风速与风向
        self.ax_wind_speed.plot(times, wind_speeds, marker='o', label="风速", color='red')
        for i, direction in enumerate(wind_directions):
            self.ax_wind_speed.annotate(direction, (times[i], wind_speeds[i]), textcoords="offset points", xytext=(0, 10), ha='center')
        self.ax_wind_speed.set_title("风速与风向")
        self.ax_wind_speed.set_xlabel("时间 (小时)")
        self.ax_wind_speed.set_ylabel("风速 (km/h)")
        self.ax_wind_speed.grid(True)

        # 云量
        self.ax_clouds.plot(times, clouds, marker='o', label="云量", color='brown')
        self.ax_clouds.set_title("云量")
        self.ax_clouds.set_xlabel("时间 (小时)")
        self.ax_clouds.set_ylabel("云量 (%)")
        self.ax_clouds.grid(True)

        # 露点温度
        if any(dew_points):  # 检查是否有有效的露点温度数据
            self.ax_dew_point.plot(times, [dp if dp is not None else 0 for dp in dew_points], marker='o', label="露点温度", color='cyan')
            self.ax_dew_point.set_title("露点温度")
            self.ax_dew_point.set_xlabel("时间 (小时)")
            self.ax_dew_point.set_ylabel("露点温度 (°C)")
            self.ax_dew_point.grid(True)
        else:
            self.ax_dew_point.text(0.5, 0.5, "暂无露点温度数据", transform=self.ax_dew_point.transAxes, ha='center', va='center', fontsize=12, color='red')

        self.canvas.draw()

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key
    window = HourlyHistory(api_client)
    window.show()
    sys.exit(app.exec())
