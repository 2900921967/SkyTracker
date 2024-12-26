import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QLineEdit, QWidget, QMessageBox


class CurrentWeather(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("天气实况")
        self.setFixedSize(400, 600)

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
                f"<h2>城市: {city}</h2>"
                f"<p><b>国家:</b> {country} <br>"
                f"<b>时区:</b> {timezone}</p>"
                f"<hr>"
                f"<h3>天气详情:</h3>"
                f"<p><b>天气:</b> {text} <br>"
                f"<b>温度:</b> {temperature}°C <br>"
                f"<b>体感温度:</b> {feels_like}°C <br>"
                f"<b>气压:</b> {pressure} mb <br>"
                f"<b>相对湿度:</b> {humidity}% <br>"
                f"<b>能见度:</b> {visibility} km</p>"
                f"<hr>"
                f"<h3>风况:</h3>"
                f"<p><b>风向:</b> {wind_direction} ({wind_direction_degree}°) <br>"
                f"<b>风速:</b> {wind_speed} km/h <br>"
                f"<b>风力等级:</b> {wind_scale}</p>"
                f"<hr>"
                f"<h3>其他信息:</h3>"
                f"<p><b>云量:</b> {clouds}% <br>"
                f"<b>露点温度:</b> {dew_point}°C <br>"
                f"<b>数据更新时间:</b> {last_update}</p>"
            )

            self.label_info.setText(info)
            self.label_info.setStyleSheet("QLabel { font-size: 14px; }")
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
