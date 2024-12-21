import sys
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QPushButton, QLineEdit, QWidget, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt

class HourlyForecast(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("24小时逐小时天气预报")
        self.setFixedSize(400, 600)

        self.data = []  # 保存逐小时天气数据
        self.current_index = 0  # 当前显示的小时索引

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

        # 显示天气信息
        self.weather_info = QLabel("点击按钮获取逐小时天气预报")
        self.weather_info.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.weather_info)

        # 切换小时按钮
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("上一小时")
        self.prev_button.clicked.connect(self.show_previous_hour)
        self.prev_button.setEnabled(False)
        nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("下一小时")
        self.next_button.clicked.connect(self.show_next_hour)
        self.next_button.setEnabled(False)
        nav_layout.addWidget(self.next_button)

        layout.addLayout(nav_layout)

        # 获取天气按钮
        btn_fetch = QPushButton("获取逐小时天气预报")
        btn_fetch.clicked.connect(self.fetch_hourly_forecast)
        layout.addWidget(btn_fetch)

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

            self.current_index = 0
            self.update_weather_info()
            self.prev_button.setEnabled(True)
            self.next_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取天气数据失败: {e}")

    def update_weather_info(self):
        if not self.data:
            return

        current_hour = self.data[self.current_index]
        time = current_hour.get('time', '暂无数据')
        text = current_hour.get('text', '暂无数据')
        temperature = current_hour.get('temperature', '暂无数据')
        humidity = current_hour.get('humidity', '暂无数据')
        wind_direction = current_hour.get('wind_direction', '暂无数据')
        wind_speed = current_hour.get('wind_speed', '暂无数据')

        info = (
            f"时间: {time}\n"
            f"天气: {text}\n"
            f"温度: {temperature}°C\n"
            f"湿度: {humidity}%\n"
            f"风向: {wind_direction}\n"
            f"风速: {wind_speed} km/h"
        )

        self.weather_info.setText(info)

    def show_previous_hour(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_weather_info()
        else:
            QMessageBox.information(self, "提示", "已经是最早的数据！")

    def show_next_hour(self):
        if self.current_index < len(self.data) - 1:
            self.current_index += 1
            self.update_weather_info()
        else:
            QMessageBox.information(self, "提示", "已经是最晚的数据！")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key
    window = HourlyForecast(api_client)
    window.show()
    sys.exit(app.exec())