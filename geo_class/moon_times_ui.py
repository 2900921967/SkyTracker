import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

class MoonTimes(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("月出月落和月相查询")
        self.setFixedSize(600, 400)

        self.data = []
        self.current_day_index = 0

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("请输入城市名称，例如: 北京")
        layout.addWidget(self.location_input)

        self.days_input = QLineEdit()
        self.days_input.setPlaceholderText("请输入查询天数，最多15天")
        layout.addWidget(self.days_input)

        self.fetch_button = QPushButton("获取月出月落和月相")
        self.fetch_button.clicked.connect(self.fetch_moon_times)
        layout.addWidget(self.fetch_button)

        self.info_label = QLabel("月出月落和月相信息")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)

        self.prev_button = QPushButton("上一天")
        self.prev_button.clicked.connect(self.show_previous_day)
        layout.addWidget(self.prev_button)

        self.next_button = QPushButton("下一天")
        self.next_button.clicked.connect(self.show_next_day)
        layout.addWidget(self.next_button)

        self.setLayout(layout)

    def fetch_moon_times(self):
        location = self.location_input.text().strip()
        days = self.days_input.text().strip()

        if not location:
            QMessageBox.warning(self, "警告", "城市名称不能为空！")
            return

        if not days.isdigit() or int(days) < 1 or int(days) > 15:
            QMessageBox.warning(self, "警告", "天数必须为1到15之间的数字！")
            return

        try:
            data = self.api_client.fetch_moon_times(location, days=int(days))
            if not data:
                QMessageBox.information(self, "提示", "当前暂无月出月落和月相数据！")
                self.info_label.setText("当前暂无月出月落和月相数据！")
                return

            self.data = data.get('moon', [])
            if not self.data:
                QMessageBox.information(self, "提示", "当前城市暂无月出月落和月相数据！")
                self.info_label.setText("当前城市暂无月出月落和月相数据！")
                return

            self.current_day_index = 0
            self.display_moon_times_for_day()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取月出月落和月相数据失败: {e}")

    def display_moon_times_for_day(self):
        if not self.data:
            return

        day_data = self.data[self.current_day_index]
        date = day_data.get('date', '暂无日期')
        rise = day_data.get('rise', '暂无数据')
        set_time = day_data.get('set', '暂无数据')
        fraction = day_data.get('fraction', '暂无数据')
        phase = day_data.get('phase', '暂无数据')
        phase_name = day_data.get('phase_name', '暂无数据')

        info = (
            f"日期: {date}\n"
            f"月出时间: {rise}\n"
            f"月落时间: {set_time}\n"
            f"月亮被照明比例: {fraction}\n"
            f"月相: {phase}\n"
            f"月相名称: {phase_name}"
        )

        self.info_label.setText(info)

    def show_previous_day(self):
        if self.current_day_index > 0:
            self.current_day_index -= 1
            self.display_moon_times_for_day()
        else:
            QMessageBox.information(self, "提示", "已经是第一天的数据！")

    def show_next_day(self):
        if self.current_day_index < len(self.data) - 1:
            self.current_day_index += 1
            self.display_moon_times_for_day()
        else:
            QMessageBox.information(self, "提示", "已经是最后一天的数据！")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = MoonTimes(api_client)
    window.show()
    sys.exit(app.exec())
