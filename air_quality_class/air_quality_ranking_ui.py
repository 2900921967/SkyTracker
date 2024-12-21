import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt

class AirQualityRanking(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("空气质量实况城市排行")
        self.setFixedSize(400, 600)

        self.data = []  # 保存城市排名数据
        self.current_index = 0  # 当前显示的城市排名索引

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 显示城市排名信息
        self.ranking_info = QLabel("点击按钮获取空气质量排名")
        self.ranking_info.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.ranking_info.setWordWrap(True)
        layout.addWidget(self.ranking_info)

        # 切换排名按钮
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("上一名")
        self.prev_button.clicked.connect(self.show_previous_city)
        self.prev_button.setEnabled(False)
        nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("下一名")
        self.next_button.clicked.connect(self.show_next_city)
        self.next_button.setEnabled(False)
        nav_layout.addWidget(self.next_button)

        layout.addLayout(nav_layout)

        # 获取排名按钮
        btn_fetch = QPushButton("获取空气质量排名")
        btn_fetch.clicked.connect(self.fetch_air_quality_ranking)
        layout.addWidget(btn_fetch)

        self.setLayout(layout)

    def fetch_air_quality_ranking(self):
        try:
            ranking_data = self.api_client.fetch_air_quality_ranking()
            self.data = ranking_data.get('results', [])
            if not self.data:
                QMessageBox.warning(self, "提示", "暂无城市空气质量排名数据！")
                self.ranking_info.setText("暂无城市空气质量排名数据！")
                self.prev_button.setEnabled(False)
                self.next_button.setEnabled(False)
                return

            self.current_index = 0
            self.update_ranking_info()
            self.prev_button.setEnabled(True)
            self.next_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取空气质量排名数据失败: {e}")

    def update_ranking_info(self):
        if not self.data:
            return

        current_city = self.data[self.current_index]
        location = current_city.get('location', {})
        aqi = current_city.get('aqi', '暂无数据')

        city_name = location.get('name', '暂无数据')
        country = location.get('country', '暂无数据')
        path = location.get('path', '暂无数据')
        timezone = location.get('timezone', '暂无数据')
        timezone_offset = location.get('timezone_offset', '暂无数据')

        info = (
            f"城市: {city_name}\n"
            f"国家: {country}\n"
            f"位置: {path}\n"
            f"时区: {timezone} (UTC{timezone_offset})\n"
            f"空气质量指数 (AQI): {aqi}"
        )

        self.ranking_info.setText(info)

    def show_previous_city(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_ranking_info()
        else:
            QMessageBox.information(self, "提示", "已经是第一名的数据！")

    def show_next_city(self):
        if self.current_index < len(self.data) - 1:
            self.current_index += 1
            self.update_ranking_info()
        else:
            QMessageBox.information(self, "提示", "已经是最后一名的数据！")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = AirQualityRanking(api_client)
    window.show()
    sys.exit(app.exec())
