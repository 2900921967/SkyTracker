import sys

import matplotlib
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

class HourlyTides(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("逐小时潮汐预报")
        self.setFixedSize(800, 800)

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

        self.canvas = FigureCanvas(Figure(figsize=(8, 4)))
        layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.add_subplot(111)

        button_layout = QHBoxLayout()
        # 上一天按钮
        self.prev_button = QPushButton("上一天")
        self.prev_button.clicked.connect(self.show_previous_day)
        button_layout.addWidget(self.prev_button)

        # 下一天按钮
        self.next_button = QPushButton("下一天")
        self.next_button.clicked.connect(self.show_next_day)
        button_layout.addWidget(self.next_button)

        layout.addLayout(button_layout)

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
                return

            # 解析数据
            self.data = data.get('data', [])
            if not self.data:
                QMessageBox.information(self, "提示", "当前港口暂无潮汐数据！")
                return

            self.current_day_index = 0
            self.display_tides_for_day()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取潮汐预报数据失败: {e}")

    def display_tides_for_day(self):
        if not self.data:
            return

        day_data = self.data[self.current_day_index]
        tide_heights = day_data.get('tide', [])

        # 转换潮汐高度为浮点数
        try:
            tide_heights = [float(height) for height in tide_heights]
        except ValueError:
            QMessageBox.critical(self, "错误", "潮汐高度数据格式有误，无法转换为数值！")
            return

        self.plot_tide_chart(tide_heights)

    def plot_tide_chart(self, tide_heights):
        self.ax.clear()
        self.ax.plot(range(len(tide_heights)), tide_heights, marker='o')
        self.ax.set_title("逐小时潮汐高度")
        self.ax.set_xlabel("时间 (小时)")
        self.ax.set_ylabel("潮高 (cm)")
        self.ax.grid(True)
        self.canvas.draw()

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
