import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt

class LifestyleIndex(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("生活指数")
        self.setFixedSize(400, 600)

        self.data = []  # 保存生活指数数据
        self.current_index = 0  # 当前显示的生活指数索引

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入框：城市名称
        self.input_city = QLineEdit()
        self.input_city.setPlaceholderText("请输入城市名称，例如: 上海")
        layout.addWidget(self.input_city)

        # 显示生活指数信息
        self.life_index_info = QLabel("点击按钮获取生活指数")
        self.life_index_info.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.life_index_info.setWordWrap(True)
        layout.addWidget(self.life_index_info)

        # 切换生活指数按钮
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("上一个")
        self.prev_button.clicked.connect(self.show_previous_index)
        self.prev_button.setEnabled(False)
        nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("下一个")
        self.next_button.clicked.connect(self.show_next_index)
        self.next_button.setEnabled(False)
        nav_layout.addWidget(self.next_button)

        layout.addLayout(nav_layout)

        # 获取生活指数按钮
        btn_fetch = QPushButton("获取生活指数")
        btn_fetch.clicked.connect(self.fetch_lifestyle_index)
        layout.addWidget(btn_fetch)

        self.setLayout(layout)

    def fetch_lifestyle_index(self):
        city = self.input_city.text().strip()

        if not city:
            QMessageBox.warning(self, "警告", "城市名称不能为空！")
            return

        try:
            # 获取生活指数数据
            life_data = self.api_client.fetch_lifestyle_index(location=city)
            if not life_data:
                QMessageBox.information(self, "提示", "当前城市暂无生活指数数据！")
                self.life_index_info.setText("当前城市暂无生活指数数据！")
                self.prev_button.setEnabled(False)
                self.next_button.setEnabled(False)
                return

            # 将生活指数转换为列表形式（排除日期字段）
            self.data = [(key, value) for key, value in life_data.items() if key != "date"]
            self.current_index = 0
            self.update_life_index_info()
            self.prev_button.setEnabled(True)
            self.next_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取生活指数数据失败: {e}")

    def update_life_index_info(self):
        if not self.data:
            self.life_index_info.setText("暂无生活指数数据！")
            return

        key, value = self.data[self.current_index]
        brief = value.get('brief', '暂无数据')
        details = value.get('details', '暂无数据')

        info = (
            f"指数名称: {key}\n"
            f"简要建议: {brief}\n"
            f"详细建议: {details}"
        )

        self.life_index_info.setText(info)

    def show_previous_index(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_life_index_info()
        else:
            QMessageBox.information(self, "提示", "已经是第一条数据！")

    def show_next_index(self):
        if self.current_index < len(self.data) - 1:
            self.current_index += 1
            self.update_life_index_info()
        else:
            QMessageBox.information(self, "提示", "已经是最后一条数据！")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = LifestyleIndex(api_client)
    window.show()
    sys.exit(app.exec())
