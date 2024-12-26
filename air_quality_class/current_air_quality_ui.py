import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

class CurrentAirQuality(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("空气质量实况")
        self.setFixedSize(400, 400)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入框：城市名称
        self.input_city = QLineEdit()
        self.input_city.setPlaceholderText("请输入城市名称，例如: 北京")
        layout.addWidget(self.input_city)

        # 显示空气质量信息
        self.air_quality_info = QLabel("点击按钮获取空气质量实况")
        self.air_quality_info.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.air_quality_info.setWordWrap(True)
        layout.addWidget(self.air_quality_info)

        # 获取空气质量按钮
        btn_fetch = QPushButton("获取空气质量实况")
        btn_fetch.clicked.connect(self.fetch_air_quality)
        layout.addWidget(btn_fetch)

        self.setLayout(layout)

    def fetch_air_quality(self):
        city = self.input_city.text().strip()

        if not city:
            QMessageBox.warning(self, "警告", "城市名称不能为空！")
            return

        try:
            air_data = self.api_client.fetch_current_air_quality(location=city)
            self.update_air_quality_info(air_data)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取空气质量数据失败: {e}")

    def update_air_quality_info(self, data):
        results = data.get('results', [{}])[0]
        location = results.get('location', {})
        air = results.get('air', {}).get('city', {})

        city_name = location.get('name', '暂无数据')
        aqi = air.get('aqi', '暂无数据')
        pm25 = air.get('pm25', '暂无数据')
        pm10 = air.get('pm10', '暂无数据')
        so2 = air.get('so2', '暂无数据')
        no2 = air.get('no2', '暂无数据')
        co = air.get('co', '暂无数据')
        o3 = air.get('o3', '暂无数据')
        primary_pollutant = air.get('primary_pollutant', '暂无数据')
        last_update = air.get('last_update', '暂无数据')
        quality = air.get('quality', '暂无数据')

        quality_color = self.get_quality_color(quality)

        info = (
            f"<h2><b>城市:</b> {city_name}</h2>"
            f"<p><b>空气质量指数 (AQI):</b> {aqi}</p>"
            f"<p><b>PM2.5:</b> {pm25}</p>"
            f"<p><b>PM10:</b> {pm10}</p>"
            f"<p><b>SO<sub>2</sub>:</b> {so2}</p>"
            f"<p><b>NO<sub>2</sub>:</b> {no2}</p>"
            f"<p><b>CO:</b> {co}</p>"
            f"<p><b>O<sub>3</sub>:</b> {o3}</p>"
            f"<p><b>主要污染物:</b> {primary_pollutant}</p>"
            f"<p><b>空气质量:</b> <span style='color:{quality_color}'>{quality}</span></p>"
            f"<p><b>最后更新时间:</b> {last_update}</p>"
        )

        self.air_quality_info.setTextFormat(Qt.TextFormat.RichText)
        self.air_quality_info.setText(info)

    def get_quality_color(self, quality):
        if quality == "优":
            return "green"
        elif quality == "良":
            return "blue"
        elif quality == "轻度污染":
            return "yellow"
        elif quality == "中度污染":
            return "orange"
        elif quality == "重度污染":
            return "red"
        elif quality == "严重污染":
            return "purple"
        return "black"

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = CurrentAirQuality(api_client)
    window.show()
    sys.exit(app.exec())
