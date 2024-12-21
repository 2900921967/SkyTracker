import sys
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QGroupBox, QApplication
from life_class.life_index_ui import LifestyleIndex
from life_class.lunar_calendar_ui import LunarCalendar
from life_class.vehicle_restriction_ui import VehicleRestriction

class LifestyleClass(QMainWindow):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("生活类功能")
        self.setFixedSize(450, 350)

        self.init_ui()

        # 子功能窗口实例
        self.lifestyle_index_window = None
        self.lunar_calendar_window = None
        self.traffic_restriction_window = None

    def init_ui(self):
        main_layout = QVBoxLayout()

        # 功能模块分组
        group_box = QGroupBox("生活功能模块")
        group_box_layout = QVBoxLayout()

        # 生活指数按钮
        btn_lifestyle_index = QPushButton("生活指数")
        btn_lifestyle_index.clicked.connect(self.open_lifestyle_index)
        group_box_layout.addWidget(btn_lifestyle_index)

        # 农历节气生肖按钮
        btn_lunar_calendar = QPushButton("农历节气生肖")
        btn_lunar_calendar.clicked.connect(self.open_lunar_calendar)
        group_box_layout.addWidget(btn_lunar_calendar)

        # 机动车尾号限行按钮
        btn_traffic_restriction = QPushButton("机动车尾号限行")
        btn_traffic_restriction.clicked.connect(self.open_traffic_restriction)
        group_box_layout.addWidget(btn_traffic_restriction)

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

    def open_lifestyle_index(self):
        if not self.lifestyle_index_window:
            self.lifestyle_index_window = LifestyleIndex(self.api_client)
        self.lifestyle_index_window.show()

    def open_lunar_calendar(self):
        if not self.lunar_calendar_window:
            self.lunar_calendar_window = LunarCalendar(self.api_client)
        self.lunar_calendar_window.show()

    def open_traffic_restriction(self):
        if not self.traffic_restriction_window:
            self.traffic_restriction_window = VehicleRestriction(self.api_client)
        self.traffic_restriction_window.show()

if __name__ == "__main__":
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = LifestyleClass(api_client)
    window.show()
    sys.exit(app.exec())
