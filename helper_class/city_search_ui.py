import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox
)


class CitySearch(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("城市搜索")
        self.setFixedSize(400, 300)

        self.results = []
        self.current_index = 0

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入框
        self.label_prompt = QLabel("请输入城市名称:")
        layout.addWidget(self.label_prompt)

        self.input_city = QLineEdit()
        self.input_city.setPlaceholderText("例如: 北京")
        layout.addWidget(self.input_city)

        # 搜索按钮
        self.button_search = QPushButton("搜索")
        self.button_search.clicked.connect(self.search_city)
        layout.addWidget(self.button_search)

        # 显示结果的标签
        self.label_info = QLabel("结果将显示在这里")
        layout.addWidget(self.label_info)

        # 上一个/下一个按钮
        nav_layout = QHBoxLayout()

        self.button_previous = QPushButton("上一个")
        self.button_previous.clicked.connect(self.show_previous)
        self.button_previous.setEnabled(False)
        nav_layout.addWidget(self.button_previous)

        self.button_next = QPushButton("下一个")
        self.button_next.clicked.connect(self.show_next)
        self.button_next.setEnabled(False)
        nav_layout.addWidget(self.button_next)

        layout.addLayout(nav_layout)

        self.setLayout(layout)

    def search_city(self):
        city_name = self.input_city.text().strip()
        if not city_name:
            QMessageBox.warning(self, "警告", "城市名称不能为空！")
            return

        try:
            data = self.api_client.search_city(city_name)
            self.results = data.get('results', [])

            if not self.results:
                QMessageBox.information(self, "提示", "未找到任何结果！")
                self.label_info.setText("未找到任何结果！")
                self.button_previous.setEnabled(False)
                self.button_next.setEnabled(False)
                return

            self.current_index = 0
            self.display_result()
            self.button_previous.setEnabled(True)
            self.button_next.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"搜索城市失败: {e}")

    def display_result(self):
        if not self.results:
            self.label_info.setText("没有可显示的结果！")
            return

        result = self.results[self.current_index]
        info = (
            f"<p><b>城市ID:</b> {result.get('id', '暂无数据')}</p>"
            f"<p><b>城市名称:</b> {result.get('name', '暂无数据')}</p>"
            f"<p><b>国家:</b> {result.get('country', '暂无数据')}</p>"
            f"<p><b>路径:</b> {result.get('path', '暂无数据')}</p>"
            f"<p><b>时区:</b> {result.get('timezone', '暂无数据')}</p>"
            f"<p><b>时区偏移:</b> {result.get('timezone_offset', '暂无数据')}</p>"
        )
        self.label_info.setTextFormat(Qt.TextFormat.RichText)
        self.label_info.setText(info)

    def show_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_result()
        else:
            QMessageBox.information(self, "提示", "已经是第一个数据！")

    def show_next(self):
        if self.current_index < len(self.results) - 1:
            self.current_index += 1
            self.display_result()
        else:
            QMessageBox.information(self, "提示", "已经是最后一个数据！")

if __name__ == "__main__":
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = CitySearch(api_client)
    window.show()
    sys.exit(app.exec())
