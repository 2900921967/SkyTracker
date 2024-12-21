import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

class HourlyTides(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("逐小时潮汐预报")
        self.setFixedSize(600, 800)

        self.data = []
        self.current_day_index = 0

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("请输入港口名称，例如: 永兴岛")
        layout.addWidget(self.port_input)

        self.fetch_button = QPushButton("获取潮汐数据")
        self.fetch_button.clicked.connect(self.fetch_tides_data)
        layout.addWidget(self.fetch_button)

        self.info_label = QLabel("逐小时潮汐预报")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)

        # 上一天按钮
        self.prev_button = QPushButton("上一天")
        self.prev_button.clicked.connect(self.show_previous_day)
        layout.addWidget(self.prev_button)

        # 下一天按钮
        self.next_button = QPushButton("下一天")
        self.next_button.clicked.connect(self.show_next_day)
        layout.addWidget(self.next_button)

        self.setLayout(layout)

    def fetch_tides_data(self):
        port = self.port_input.text().strip()
        if not port:
            QMessageBox.warning(self, "警告", "港口名称不能为空！")
            return

        try:
            # 调用 API 获取数据
            data = self.api_client.fetch_tides_forecast(port)
            if not data:
                QMessageBox.information(self, "提示", "当前暂无潮汐预报数据！")
                self.info_label.setText("当前暂无潮汐预报数据！")
                return

            # 解析数据
            self.data = data.get('data', [])
            if not self.data:
                QMessageBox.information(self, "提示", "当前港口暂无潮汐数据！")
                self.info_label.setText("当前港口暂无潮汐数据！")
                return

            self.current_day_index = 0
            self.display_tides_for_day()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取潮汐预报数据失败: {e}")

    def display_tides_for_day(self):
        if not self.data:
            return

        day_data = self.data[self.current_day_index]
        date = day_data.get('date', '暂无日期')
        tide_heights = day_data.get('tide', [])
        ranges = day_data.get('range', [])

        tide_info = f"日期: {date}\n\n逐小时潮汐高度:\n"
        for hour, height in enumerate(tide_heights):
            tide_info += f"{hour:02d}:00 - {height} cm\n"

        tide_info += "\n高低潮信息:\n"
        for range_info in ranges:
            time = range_info.get('time', '暂无时间')
            height = range_info.get('height', '暂无高度')
            type_ = range_info.get('type', '暂无类型')
            tide_info += f"时间: {time}, 潮高: {height} cm, 类型: {type_}\n"

        self.info_label.setText(tide_info)

    def show_previous_day(self):
        if self.current_day_index > 0:
            self.current_day_index -= 1
            self.display_tides_for_day()
        else:
            QMessageBox.information(self, "提示", "已经是第一天的数据！")

    def show_next_day(self):
        if self.current_day_index < len(self.data) - 1:
            self.current_day_index += 1
            self.display_tides_for_day()
        else:
            QMessageBox.information(self, "提示", "已经是最后一天的数据！")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = HourlyTides(api_client)
    window.show()
    sys.exit(app.exec())
