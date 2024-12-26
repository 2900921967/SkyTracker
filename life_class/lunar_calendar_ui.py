import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

class LunarCalendar(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("农历节气生肖")
        self.setFixedSize(400, 350)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 显示农历节气生肖信息
        self.info_label = QLabel("点击按钮获取农历节气生肖信息")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)

        # 获取信息按钮
        fetch_button = QPushButton("获取信息")
        fetch_button.clicked.connect(self.fetch_lunar_calendar)
        layout.addWidget(fetch_button)

        self.setLayout(layout)

    def fetch_lunar_calendar(self):
        try:
            # 调用 API 获取数据
            data = self.api_client.fetch_lunar_calendar()
            if not data:
                QMessageBox.information(self, "提示", "当前暂无农历节气生肖信息！")
                self.info_label.setText("当前暂无农历节气生肖信息！")
                return

            # 解析数据
            calendar_data = data
            date = calendar_data.get('date', '暂无数据')
            zodiac = calendar_data.get('zodiac', '暂无数据')
            ganzhi_year = calendar_data.get('ganzhi_year', '暂无数据')
            ganzhi_month = calendar_data.get('ganzhi_month', '暂无数据')
            ganzhi_day = calendar_data.get('ganzhi_day', '暂无数据')
            lunar_year = calendar_data.get('lunar_year', '暂无数据')
            lunar_month_name = calendar_data.get('lunar_month_name', '暂无数据')
            lunar_day_name = calendar_data.get('lunar_day_name', '暂无数据')
            lunar_festival = calendar_data.get('lunar_festival', '暂无数据')
            solar_term = calendar_data.get('solar_term', '暂无数据')

            info = (
                f"<p><b>公历日期:</b> {date}</p>"
                f"<p><b>生肖属相:</b> {zodiac}</p>"
                f"<p><b>干支纪年:</b> {ganzhi_year}</p>"
                f"<p><b>干支纪月:</b> {ganzhi_month}</p>"
                f"<p><b>干支纪日:</b> {ganzhi_day}</p>"
                f"<p><b>农历年:</b> {lunar_year}</p>"
                f"<p><b>农历月:</b> {lunar_month_name}</p>"
                f"<p><b>农历日:</b> {lunar_day_name}</p>"
                f"<p><b>农历节日:</b> {lunar_festival}</p>"
                f"<p><b>二十四节气:</b> {solar_term}</p>"
            )

            self.info_label.setTextFormat(Qt.TextFormat.RichText)
            self.info_label.setText(info)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取农历节气生肖数据失败: {e}")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = LunarCalendar(api_client)
    window.show()
    sys.exit(app.exec())
