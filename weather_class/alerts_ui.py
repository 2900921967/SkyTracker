import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QPushButton, QLineEdit, QWidget, QMessageBox, QHBoxLayout
)


class WeatherAlerts(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("气象灾害预警")
        self.setFixedSize(400, 400)

        self.data = []  # 保存气象灾害预警数据
        self.current_index = 0  # 当前显示的预警索引

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入框：城市名称
        self.input_city = QLineEdit()
        self.input_city.setPlaceholderText("请输入城市名称，例如: 北京")
        layout.addWidget(self.input_city)

        # 显示预警信息
        self.alert_info = QLabel("点击按钮获取气象灾害预警")
        self.alert_info.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.alert_info.setWordWrap(True)
        layout.addWidget(self.alert_info)

        # 切换预警按钮
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("上一预警")
        self.prev_button.clicked.connect(self.show_previous_alert)
        self.prev_button.setEnabled(False)
        nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("下一预警")
        self.next_button.clicked.connect(self.show_next_alert)
        self.next_button.setEnabled(False)
        nav_layout.addWidget(self.next_button)

        layout.addLayout(nav_layout)

        # 获取预警按钮
        btn_fetch = QPushButton("获取气象灾害预警")
        btn_fetch.clicked.connect(self.fetch_alerts)
        layout.addWidget(btn_fetch)

        self.setLayout(layout)

    def fetch_alerts(self):
        city = self.input_city.text().strip()

        if not city:
            QMessageBox.warning(self, "警告", "城市名称不能为空！")
            return

        try:
            weather_data = self.api_client.fetch_weather_alerts(location=city)
            self.data = weather_data.get('results', [{}])[0].get('alarms', [])
            if not self.data:
                QMessageBox.information(self, "提示", "当前城市暂无预警信息！")
                self.alert_info.setText("当前城市暂无预警信息！")
                self.prev_button.setEnabled(False)
                self.next_button.setEnabled(False)
                return

            self.current_index = 0
            self.update_alert_info()
            self.prev_button.setEnabled(True)
            self.next_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取预警信息失败: {e}")

    def update_alert_info(self):
        if not self.data:
            return

        current_alert = self.data[self.current_index]
        title = current_alert.get('title', '暂无数据')
        type_ = current_alert.get('type', '暂无数据')
        level = current_alert.get('level', '暂无数据')
        description = current_alert.get('description', '暂无数据')
        pub_date = current_alert.get('pub_date', '暂无数据')

        color = self.get_level_color(level)

        info = (
            f"<h2>预警标题: {title}</h2>"
            f"<p><b>预警类型:</b> {type_}</p>"
            f"<p><b>预警级别:</b> <span style='color:{color}'>{level}</span></p>"
            f"<p><b>详细描述:</b></p>"
            f"<p style='margin-left:20px;'>{description}</p>"
            f"<p><b>发布时间:</b> {pub_date}</p>"
        )

        self.alert_info.setTextFormat(Qt.TextFormat.RichText)
        self.alert_info.setText(info)

    def get_level_color(self, level):
        if level == "蓝色":
            return "blue"
        elif level == "黄色":
            return "yellow"
        elif level == "橙色":
            return "orange"
        elif level == "红色":
            return "red"
        return "black"

    def show_previous_alert(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_alert_info()
        else:
            QMessageBox.information(self, "提示", "已经是第一条预警！")

    def show_next_alert(self):
        if self.current_index < len(self.data) - 1:
            self.current_index += 1
            self.update_alert_info()
        else:
            QMessageBox.information(self, "提示", "已经是最后一条预警！")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key
    window = WeatherAlerts(api_client)
    window.show()
    sys.exit(app.exec())
