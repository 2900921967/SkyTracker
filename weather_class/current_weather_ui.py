import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QLineEdit, QWidget, QMessageBox

class CurrentWeather(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("天气实况")
        self.setFixedSize(400, 500)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.input_city = QLineEdit()
        self.input_city.setPlaceholderText("请输入城市名称，例如: 北京")
        layout.addWidget(self.input_city)

        self.label_info = QLabel("点击按钮获取天气实况")
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.label_info.setWordWrap(True)
        layout.addWidget(self.label_info)

        btn_fetch = QPushButton("获取天气实况")
        btn_fetch.clicked.connect(self.fetch_weather_data)
        layout.addWidget(btn_fetch)

        self.setLayout(layout)

    def fetch_weather_data(self):
        location = self.input_city.text().strip()
        if not location:
            QMessageBox.warning(self, "警告", "城市名称不能为空！")
            return

        try:
            weather_data = self.api_client.fetch_current_weather(location=location)
            self.display_weather(weather_data)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取天气数据失败: {e}")

    def display_weather(self, data):
        try:
            result = data.get('results', [{}])[0]
            location = result.get('location', {})
            now = result.get('now', {})

            city = location.get('name', '暂无数据')
            country = location.get('country', '暂无数据')
            timezone = location.get('timezone', '暂无数据')

            text = now.get('text', '暂无数据')
            temperature = now.get('temperature', '暂无数据')
            feels_like = now.get('feels_like', '暂无数据')
            pressure = now.get('pressure', '暂无数据')
            humidity = now.get('humidity', '暂无数据')
            visibility = now.get('visibility', '暂无数据')
            wind_direction = now.get('wind_direction', '暂无数据')
            wind_direction_degree = now.get('wind_direction_degree', '暂无数据')
            wind_speed = now.get('wind_speed', '暂无数据')
            wind_scale = now.get('wind_scale', '暂无数据')
            clouds = now.get('clouds', '暂无数据')
            dew_point = now.get('dew_point', '暂无数据')

            last_update = result.get('last_update', '暂无数据')

            info = (
                f"城市: {city}\n"
                f"国家: {country}\n"
                f"时区: {timezone}\n\n"
                f"天气: {text}\n"
                f"温度: {temperature}°C\n"
                f"体感温度: {feels_like}°C\n"
                f"气压: {pressure} mb\n"
                f"相对湿度: {humidity}%\n"
                f"能见度: {visibility} km\n"
                f"风向: {wind_direction} ({wind_direction_degree}°)\n"
                f"风速: {wind_speed} km/h\n"
                f"风力等级: {wind_scale}\n"
                f"云量: {clouds}%\n"
                f"露点温度: {dew_point}°C\n\n"
                f"数据更新时间: {last_update}"
            )

            self.label_info.setText(info)
        except KeyError:
            QMessageBox.critical(self, "错误", "解析天气数据失败！")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key
    window = CurrentWeather(api_client)
    window.show()
    sys.exit(app.exec())
