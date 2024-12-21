import sys
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QGroupBox, QApplication
from geo_class.sun_times_ui import SunriseSunset
from geo_class.moon_times_ui import MoonTimes

class GeoClass(QMainWindow):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("地理类功能")
        self.setFixedSize(450, 350)

        self.init_ui()

        # 子功能窗口实例
        self.sunrise_sunset_window = None
        self.moonrise_moonset_window = None

    def init_ui(self):
        main_layout = QVBoxLayout()

        # 功能模块分组
        group_box = QGroupBox("地理功能模块")
        group_box_layout = QVBoxLayout()

        # 日出日落按钮
        btn_sunrise_sunset = QPushButton("日出日落")
        btn_sunrise_sunset.clicked.connect(self.open_sunrise_sunset)
        group_box_layout.addWidget(btn_sunrise_sunset)

        # 月出月落月相按钮
        btn_moonrise_moonset = QPushButton("月出月落月相")
        btn_moonrise_moonset.clicked.connect(self.open_moonrise_moonset)
        group_box_layout.addWidget(btn_moonrise_moonset)

        group_box.setLayout(group_box_layout)
        main_layout.addWidget(group_box)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # 样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
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

    def open_sunrise_sunset(self):
        if not self.sunrise_sunset_window:
            self.sunrise_sunset_window = SunriseSunset(self.api_client)
        self.sunrise_sunset_window.show()

    def open_moonrise_moonset(self):
        if not self.moonrise_moonset_window:
            self.moonrise_moonset_window = MoonTimes(self.api_client)
        self.moonrise_moonset_window.show()

if __name__ == "__main__":
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = GeoClass(api_client)
    window.show()
    sys.exit(app.exec())
