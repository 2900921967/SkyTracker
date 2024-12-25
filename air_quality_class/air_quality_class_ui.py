import sys

from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QWidget, QGroupBox, QApplication
)

from air_quality_class.air_quality_ranking_ui import AirQualityRanking
from air_quality_class.current_air_quality_ui import CurrentAirQuality
from air_quality_class.daily_air_quality_ui import DailyAirQuality
from air_quality_class.hourly_air_quality_ui import HourlyAirQualityForecast


class AirQualityClass(QMainWindow):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("空气类功能")
        self.setFixedSize(450, 400)

        self.init_ui()

        # 子功能窗口实例
        self.current_air_quality_window = None
        self.city_air_ranking_window = None
        self.hourly_air_history_window = None
        self.daily_air_forecast_window = None
        self.hourly_air_forecast_window = None

    def init_ui(self):
        main_layout = QVBoxLayout()

        # 功能模块分组
        group_box = QGroupBox("空气质量功能模块")
        group_box_layout = QVBoxLayout()

        # 空气质量实况按钮
        btn_current_air_quality = QPushButton("空气质量实况")
        btn_current_air_quality.clicked.connect(self.open_current_air_quality)
        group_box_layout.addWidget(btn_current_air_quality)

        # 空气质量实况城市排行按钮
        btn_city_air_ranking = QPushButton("空气质量实况城市排行")
        btn_city_air_ranking.clicked.connect(self.open_city_air_ranking)
        group_box_layout.addWidget(btn_city_air_ranking)

        # 逐日空气质量预报按钮
        btn_daily_air_forecast = QPushButton("逐日空气质量预报")
        btn_daily_air_forecast.clicked.connect(self.open_daily_air_forecast)
        group_box_layout.addWidget(btn_daily_air_forecast)

        # 逐小时空气质量预报按钮
        btn_hourly_air_forecast = QPushButton("逐小时空气质量预报")
        btn_hourly_air_forecast.clicked.connect(self.open_hourly_air_forecast)
        group_box_layout.addWidget(btn_hourly_air_forecast)

        group_box.setLayout(group_box_layout)
        main_layout.addWidget(group_box)

        # 设置主窗口布局
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # 样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f7f7f7;
            }
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
                padding: 10px;
                border: 1px solid #d3d3d3;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                margin: 5px 0;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """)

    def open_current_air_quality(self):
        if not self.current_air_quality_window:
            self.current_air_quality_window = CurrentAirQuality(self.api_client)
        self.current_air_quality_window.show()

    def open_city_air_ranking(self):
        if not self.city_air_ranking_window:
            self.city_air_ranking_window = AirQualityRanking(self.api_client)
        self.city_air_ranking_window.show()

    def open_daily_air_forecast(self):
        if not self.daily_air_forecast_window:
            self.daily_air_forecast_window = DailyAirQuality(self.api_client)
        self.daily_air_forecast_window.show()

    def open_hourly_air_forecast(self):
        if not self.hourly_air_forecast_window:
            self.hourly_air_forecast_window = HourlyAirQualityForecast(self.api_client)
        self.hourly_air_forecast_window.show()

if __name__ == "__main__":
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = AirQualityClass(api_client)
    window.show()
    sys.exit(app.exec())
