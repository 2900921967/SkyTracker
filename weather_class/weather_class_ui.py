import sys
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QGroupBox, QApplication
from weather_class.current_weather_ui import CurrentWeather
from weather_class.daily_forecast_ui import DailyForecast
from weather_class.hourly_forecast_ui import HourlyForecast
from weather_class.hourly_history_ui import HourlyHistory
from weather_class.alerts_ui import WeatherAlerts

class WeatherClass(QMainWindow):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("天气类功能")
        self.setFixedSize(450, 400)

        self.init_ui()

        # 子功能窗口实例
        self.current_weather_window = None
        self.daily_forecast_window = None
        self.hourly_forecast_window = None
        self.hourly_history_window = None
        self.alerts_window = None

    def init_ui(self):
        main_layout = QVBoxLayout()

        # 功能模块分组
        group_box = QGroupBox("天气功能模块")
        group_box_layout = QVBoxLayout()

        # 天气实况按钮
        btn_current_weather = QPushButton("天气实况")
        btn_current_weather.clicked.connect(self.open_current_weather)
        group_box_layout.addWidget(btn_current_weather)

        # 逐日天气预报按钮
        btn_daily_forecast = QPushButton("逐日天气预报")
        btn_daily_forecast.clicked.connect(self.open_daily_forecast)
        group_box_layout.addWidget(btn_daily_forecast)

        # 24小时逐小时天气预报按钮
        btn_hourly_forecast = QPushButton("24小时逐小时天气预报")
        btn_hourly_forecast.clicked.connect(self.open_hourly_forecast)
        group_box_layout.addWidget(btn_hourly_forecast)

        # 24小时历史天气按钮
        btn_hourly_history = QPushButton("24小时历史天气")
        btn_hourly_history.clicked.connect(self.open_hourly_history)
        group_box_layout.addWidget(btn_hourly_history)

        # 气象灾害预警按钮
        btn_alerts = QPushButton("气象灾害预警")
        btn_alerts.clicked.connect(self.open_alerts)
        group_box_layout.addWidget(btn_alerts)

        group_box.setLayout(group_box_layout)
        main_layout.addWidget(group_box)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # 样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #e6f7ff;
            }
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
                padding: 10px;
                border: 1px solid #add8e6;
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

    def open_current_weather(self):
        if self.current_weather_window is None:
            self.current_weather_window = CurrentWeather(self.api_client)
        self.current_weather_window.show()

    def open_daily_forecast(self):
        if self.daily_forecast_window is None:
            self.daily_forecast_window = DailyForecast(self.api_client)
        self.daily_forecast_window.show()

    def open_hourly_forecast(self):
        if self.hourly_forecast_window is None:
            self.hourly_forecast_window = HourlyForecast(self.api_client)
        self.hourly_forecast_window.show()

    def open_hourly_history(self):
        if self.hourly_history_window is None:
            self.hourly_history_window = HourlyHistory(self.api_client)
        self.hourly_history_window.show()

    def open_alerts(self):
        if self.alerts_window is None:
            self.alerts_window = WeatherAlerts(self.api_client)
        self.alerts_window.show()

if __name__ == "__main__":
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = WeatherClass(api_client)
    window.show()
    sys.exit(app.exec())
