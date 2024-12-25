import sys

import matplotlib
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

class MoonTimes(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("月出月落和月相查询")
        self.setFixedSize(800, 800)

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

        self.fetch_button = QPushButton("获取月出月落和月相")
        self.fetch_button.clicked.connect(self.fetch_moon_times)
        layout.addWidget(self.fetch_button)

        self.canvas = FigureCanvas(Figure(figsize=(8, 10)))
        layout.addWidget(self.canvas)
        self.ax_rise = self.canvas.figure.add_subplot(411)
        self.ax_set = self.canvas.figure.add_subplot(412)
        self.ax_fraction = self.canvas.figure.add_subplot(413)
        self.ax_phase = self.canvas.figure.add_subplot(414)
        self.canvas.figure.tight_layout(pad=5.0)  # 增加图表间距

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
                return

            self.data = data.get('moon', [])
            if not self.data:
                QMessageBox.information(self, "提示", "当前城市暂无月出月落和月相数据！")
                return

            self.plot_moon_times()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取月出月落和月相数据失败: {e}")

    def plot_moon_times(self):
        if not self.data:
            return

        dates = [day['date'][5:] for day in self.data]  # 去掉年份，仅显示月-日
        rises = [self.safe_time_to_float(day['rise']) for day in self.data]
        sets = [self.safe_time_to_float(day['set']) for day in self.data]
        fractions = [float(day['fraction']) for day in self.data]
        phases = [float(day['phase']) for day in self.data]
        phase_names = [day['phase_name'] for day in self.data]

        self.ax_rise.clear()
        self.ax_set.clear()
        self.ax_fraction.clear()
        self.ax_phase.clear()

        # 月出时间
        self.ax_rise.plot(dates, rises, marker='o', label="月出时间")
        self.ax_rise.set_title("月出时间")
        self.ax_rise.set_xlabel("日期")
        self.ax_rise.set_ylabel("时间 (HH:MM)")
        self.ax_rise.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_time))
        self.ax_rise.grid(True)

        # 月落时间
        self.ax_set.plot(dates, sets, marker='o', label="月落时间", color='orange')
        self.ax_set.set_title("月落时间")
        self.ax_set.set_xlabel("日期")
        self.ax_set.set_ylabel("时间 (HH:MM)")
        self.ax_set.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_time))
        self.ax_set.grid(True)

        # 月亮被照明比例
        self.ax_fraction.plot(dates, fractions, marker='o', label="月亮被照明比例", color='green')
        self.ax_fraction.set_title("月亮被照明比例")
        self.ax_fraction.set_xlabel("日期")
        self.ax_fraction.set_ylabel("比例 (0-1)")
        self.ax_fraction.grid(True)

        # 月相
        self.ax_phase.plot(dates, phases, marker='o', label="月相", color='purple')
        for i, txt in enumerate(phase_names):
            self.ax_phase.annotate(txt, (dates[i], phases[i]), textcoords="offset points", xytext=(0, 10), ha='center')
        self.ax_phase.set_title("月相")
        self.ax_phase.set_xlabel("日期")
        self.ax_phase.set_ylabel("月相 (0-1)")
        self.ax_phase.grid(True)

        self.canvas.draw()

    @staticmethod
    def safe_time_to_float(time_str):
        """安全地将时间字符串 (HH:MM) 转换为浮点数表示的小时，处理空值"""
        if not time_str or ':' not in time_str:
            return 0.0  # 如果时间无效，返回默认值 0.0
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

    window = MoonTimes(api_client)
    window.show()
    sys.exit(app.exec())
