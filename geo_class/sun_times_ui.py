import sys

import matplotlib
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

class SunriseSunset(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("日出日落时间查询")
        self.setFixedSize(800, 600)

        self.data = []

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("请输入城市名称，例如: 北京")
        layout.addWidget(self.location_input)

        self.days_input = QLineEdit()
        self.days_input.setPlaceholderText("请输入查询天数，最多15天")
        layout.addWidget(self.days_input)

        self.fetch_button = QPushButton("获取日出日落时间")
        self.fetch_button.clicked.connect(self.fetch_sun_times)
        layout.addWidget(self.fetch_button)

        self.canvas = FigureCanvas(Figure(figsize=(8, 6)))
        layout.addWidget(self.canvas)
        self.ax_sunrise = self.canvas.figure.add_subplot(211)
        self.ax_sunset = self.canvas.figure.add_subplot(212)
        self.canvas.figure.tight_layout(pad=5.0)  # 增加图表间距

        self.setLayout(layout)

    def fetch_sun_times(self):
        location = self.location_input.text().strip()
        days = self.days_input.text().strip()

        if not location:
            QMessageBox.warning(self, "警告", "城市名称不能为空！")
            return

        if not days.isdigit() or int(days) < 1 or int(days) > 15:
            QMessageBox.warning(self, "警告", "天数必须为1到15之间的数字！")
            return

        try:
            data = self.api_client.fetch_sun_times(location, days=int(days))
            if not data:
                QMessageBox.information(self, "提示", "当前暂无日出日落数据！")
                return

            self.data = data.get('sun', [])
            if not self.data:
                QMessageBox.information(self, "提示", "当前城市暂无日出日落数据！")
                return

            self.plot_sun_times()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取日出日落数据失败: {e}")

    def plot_sun_times(self):
        if not self.data:
            return

        dates = [day['date'] for day in self.data]
        sunrises = [self.time_to_float(day['sunrise']) for day in self.data]
        sunsets = [self.time_to_float(day['sunset']) for day in self.data]

        self.ax_sunrise.clear()
        self.ax_sunset.clear()

        # 格式化日期，仅显示月-日
        dates_formatted = [date[5:] for date in dates]

        self.ax_sunrise.plot(dates_formatted, sunrises, marker='o', label="日出时间")
        self.ax_sunrise.set_title("日出时间")
        self.ax_sunrise.set_xlabel("日期")
        self.ax_sunrise.set_ylabel("时间 (24小时制)")
        self.ax_sunrise.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_time))
        self.ax_sunrise.legend()
        self.ax_sunrise.grid(True)

        self.ax_sunset.plot(dates_formatted, sunsets, marker='o', label="日落时间", color='orange')
        self.ax_sunset.set_title("日落时间")
        self.ax_sunset.set_xlabel("日期")
        self.ax_sunset.set_ylabel("时间 (24小时制)")
        self.ax_sunset.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_time))
        self.ax_sunset.legend()
        self.ax_sunset.grid(True)

        self.canvas.draw()

    @staticmethod
    def time_to_float(time_str):
        """将时间字符串 (HH:MM) 转换为浮点数表示的小时"""
        hours, minutes = map(int, time_str.split(':'))
        return hours + minutes / 60

    @staticmethod
    def format_time(value, pos):
        """将浮点数时间格式化为 HH:MM"""
        hours = int(value)
        minutes = int((value - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = SunriseSunset(api_client)
    window.show()
    sys.exit(app.exec())
