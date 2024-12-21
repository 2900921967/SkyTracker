import sys
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QPushButton, QLineEdit, QWidget, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt

class DailyForecast(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("逐日天气预报")
        self.setFixedSize(400, 600)

        self.data = []  # 保存逐日天气数据
        self.current_index = 0  # 当前显示的日期索引

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

        # 显示天气信息
        self.weather_info = QLabel("点击按钮获取逐日天气预报")
        self.weather_info.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.weather_info)

        # 切换日期按钮
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("上一天")
        self.prev_button.clicked.connect(self.show_previous_day)
        self.prev_button.setEnabled(False)
        nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("下一天")
        self.next_button.clicked.connect(self.show_next_day)
        self.next_button.setEnabled(False)
        nav_layout.addWidget(self.next_button)

        layout.addLayout(nav_layout)

        # 获取天气按钮
        btn_fetch = QPushButton("获取逐日天气预报")
        btn_fetch.clicked.connect(self.fetch_daily_forecast)
        layout.addWidget(btn_fetch)

        self.setLayout(layout)

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

            self.current_index = 0
            self.update_weather_info()
            self.prev_button.setEnabled(True)
            self.next_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取天气数据失败: {e}")

    def update_weather_info(self):
        if not self.data:
            return

        current_day = self.data[self.current_index]
        date = current_day.get('date', '暂无数据')
        text_day = current_day.get('text_day', '暂无数据')
        text_night = current_day.get('text_night', '暂无数据')
        high = current_day.get('high', '暂无数据')
        low = current_day.get('low', '暂无数据')
        precip = current_day.get('precip', '暂无数据')
        wind_direction = current_day.get('wind_direction', '暂无数据')
        wind_speed = current_day.get('wind_speed', '暂无数据')
        humidity = current_day.get('humidity', '暂无数据')

        info = (
            f"日期: {date}\n"
            f"白天天气: {text_day}\n"
            f"晚间天气: {text_night}\n"
            f"最高温度: {high}°C\n"
            f"最低温度: {low}°C\n"
            f"降水概率: {precip}%\n"
            f"风向: {wind_direction}\n"
            f"风速: {wind_speed} km/h\n"
            f"湿度: {humidity}%"
        )

        self.weather_info.setText(info)

    def show_previous_day(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_weather_info()
        else:
            QMessageBox.information(self, "提示", "已经是第一天的数据！")

    def show_next_day(self):
        if self.current_index < len(self.data) - 1:
            self.current_index += 1
            self.update_weather_info()
        else:
            QMessageBox.information(self, "提示", "已经是最后一天的数据！")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key
    window = DailyForecast(api_client)
    window.show()
    sys.exit(app.exec())
