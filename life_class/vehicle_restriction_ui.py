import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt

class VehicleRestriction(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("机动车尾号限行查询")
        self.setFixedSize(500, 550)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.info_label = QLabel("请选择城市以查询机动车尾号限行信息")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)

        # 城市按钮布局
        city_layout = QHBoxLayout()
        cities = [
            ("北京", "WX4FBXXFKE4F"),
            ("天津", "WWGQDCW6TBW1"),
            ("哈尔滨", "YB1UX38K6DY1"),
            ("成都", "WM6N2PM3WY2K"),
            ("杭州", "WTMKQ069CCJ7"),
            ("贵阳", "WKEZD7MXE04F"),
            ("长春", "WZC1EXZ0P9HU"),
            ("兰州", "WQ3V4QR6VR6G"),
            ("南昌", "WT47HJP3HEMP"),
            ("武汉", "WT3Q0FW9ZJ3Q")
        ]

        for city_name, location_id in cities:
            button = QPushButton(city_name)
            button.clicked.connect(lambda checked, loc=location_id: self.fetch_restriction_data(loc))
            city_layout.addWidget(button)

        layout.addLayout(city_layout)
        self.setLayout(layout)

    def fetch_restriction_data(self, location_id):
        try:
            # 调用 API 获取数据
            data = self.api_client.fetch_vehicle_restriction(location=location_id)
            if not data:
                QMessageBox.information(self, "提示", "当前城市暂无机动车尾号限行信息！")
                self.info_label.setText("当前城市暂无机动车尾号限行信息！")
                return

            # 解析数据
            restriction = data.get('restriction', {})
            penalty = restriction.get('penalty', '暂无数据')
            region = restriction.get('region', '暂无数据')
            remarks = restriction.get('remarks', '暂无数据')
            limits = restriction.get('limits', [])

            # 格式化限行信息
            limit_info = ""
            for limit in limits:
                date = limit.get('date', '暂无数据')
                plates = ", ".join(limit.get('plates', []))
                memo = limit.get('memo', '暂无数据')
                limit_info += (
                    f"<p><b>日期:</b> {date}<br>"
                    f"<b>限行尾号:</b> {plates}<br>"
                    f"<b>类型:</b> {memo}</p><hr>"
                )

            info = (
                f"<p><b>处罚规定:</b> {penalty}</p>"
                f"<p><b>限行区域:</b> {region}</p>"
                f"<p><b>详细说明:</b> {remarks}</p>"
                f"<h3>限行详情:</h3>"
                f"{limit_info}"
            )

            self.info_label.setTextFormat(Qt.TextFormat.RichText)
            self.info_label.setText(info)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取机动车尾号限行数据失败: {e}")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = VehicleRestriction(api_client)
    window.show()
    sys.exit(app.exec())
