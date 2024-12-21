import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt

class DailyAirQuality(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("逐日空气质量预报")
        self.setFixedSize(400, 600)

        self.data = []  # 保存逐日空气质量预报数据
        self.current_index = 0  # 当前显示的日期索引

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入框：城市名称
        self.input_city = QLineEdit()
        self.input_city.setPlaceholderText("请输入城市名称，例如: 北京")
        layout.addWidget(self.input_city)

        # 显示空气质量信息
        self.air_quality_info = QLabel("点击按钮获取逐日空气质量预报")
        self.air_quality_info.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.air_quality_info.setWordWrap(True)
        layout.addWidget(self.air_quality_info)

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

        # 获取空气质量预报按钮
        btn_fetch = QPushButton("获取逐日空气质量预报")
        btn_fetch.clicked.connect(self.fetch_daily_air_quality)
        layout.addWidget(btn_fetch)

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
                self.air_quality_info.setText("当前城市暂无空气质量预报数据！")
                self.prev_button.setEnabled(False)
                self.next_button.setEnabled(False)
                return

            self.current_index = 0
            self.update_air_quality_info()
            self.prev_button.setEnabled(True)
            self.next_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取空气质量预报数据失败: {e}")

    def update_air_quality_info(self):
        if not self.data:
            return

        current_day = self.data[self.current_index]
        date = current_day.get('date', '暂无数据')
        aqi = current_day.get('aqi', '暂无数据')
        pm25 = current_day.get('pm25', '暂无数据')
        pm10 = current_day.get('pm10', '暂无数据')
        so2 = current_day.get('so2', '暂无数据')
        no2 = current_day.get('no2', '暂无数据')
        co = current_day.get('co', '暂无数据')
        o3 = current_day.get('o3', '暂无数据')
        quality = current_day.get('quality', '暂无数据')

        # 根据空气质量等级设置颜色
        quality_color = self.get_quality_color(quality)

        info = (
            f"日期: {date}<br>"
            f"空气质量指数 (AQI): {aqi}<br>"
            f"PM2.5: {pm25}<br>"
            f"PM10: {pm10}<br>"
            f"SO2: {so2}<br>"
            f"NO2: {no2}<br>"
            f"CO: {co}<br>"
            f"O3: {o3}<br>"
            f"空气质量: <span style='color:{quality_color}'>{quality}</span>"
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

    def show_previous_day(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_air_quality_info()
        else:
            QMessageBox.information(self, "提示", "已经是第一天的数据！")

    def show_next_day(self):
        if self.current_index < len(self.data) - 1:
            self.current_index += 1
            self.update_air_quality_info()
        else:
            QMessageBox.information(self, "提示", "已经是最后一天的数据！")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = DailyAirQuality(api_client)
    window.show()
    sys.exit(app.exec())
