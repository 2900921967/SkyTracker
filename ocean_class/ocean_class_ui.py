import sys
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QGroupBox, QApplication
from ocean_class.tide_forecast_ui import HourlyTides

class OceanClass(QMainWindow):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("海洋类功能")
        self.setFixedSize(450, 300)

        self.init_ui()

        # 子功能窗口实例
        self.hourly_tides_window = None

    def init_ui(self):
        main_layout = QVBoxLayout()

        # 功能模块分组
        group_box = QGroupBox("海洋功能模块")
        group_box_layout = QVBoxLayout()

        # 逐小时潮汐预报按钮
        btn_hourly_tides = QPushButton("逐小时潮汐预报")
        btn_hourly_tides.clicked.connect(self.open_hourly_tides)
        group_box_layout.addWidget(btn_hourly_tides)

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

    def open_hourly_tides(self):
        if not self.hourly_tides_window:
            self.hourly_tides_window = HourlyTides(self.api_client)
        self.hourly_tides_window.show()

if __name__ == "__main__":
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = OceanClass(api_client)
    window.show()
    sys.exit(app.exec())
