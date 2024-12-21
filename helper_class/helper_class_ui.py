import sys
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QGroupBox, QApplication
from helper_class.city_search_ui import CitySearch

class HelperClass(QMainWindow):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("辅助类功能")
        self.setFixedSize(450, 300)

        self.init_ui()

        # 子功能窗口实例
        self.city_search_window = None

    def init_ui(self):
        main_layout = QVBoxLayout()

        # 功能模块分组
        group_box = QGroupBox("辅助功能模块")
        group_box_layout = QVBoxLayout()

        # 城市搜索按钮
        btn_city_search = QPushButton("城市搜索")
        btn_city_search.clicked.connect(self.open_city_search)
        group_box_layout.addWidget(btn_city_search)

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

    def open_city_search(self):
        if not self.city_search_window:
            self.city_search_window = CitySearch(self.api_client)
        self.city_search_window.show()

if __name__ == "__main__":
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = HelperClass(api_client)
    window.show()
    sys.exit(app.exec())
