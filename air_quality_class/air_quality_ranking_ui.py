import sys

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QMessageBox
)


class AirQualityRanking(QWidget):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("空气质量实况城市排行")
        self.setFixedSize(600, 500)  # 增加窗口宽度以适应新增列

        self.data = []  # 保存城市排名数据
        self.filtered_data = []  # 搜索过滤后的数据

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 搜索框
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("请输入城市名称搜索...")
        self.search_box.textChanged.connect(self.filter_table)
        layout.addWidget(self.search_box)

        # 表格：用于显示城市排名信息
        self.table = QTableWidget()
        self.table.setColumnCount(4)  # 四列：排名、城市、位置、空气质量指数
        self.table.setHorizontalHeaderLabels(["排名", "城市", "位置", "空气质量指数 (AQI)"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # 禁止编辑
        self.table.verticalHeader().setVisible(False)  # 隐藏行号
        layout.addWidget(self.table)

        # 获取排名按钮
        btn_fetch = QPushButton("获取空气质量排名")
        btn_fetch.clicked.connect(self.fetch_air_quality_ranking)
        layout.addWidget(btn_fetch)

        self.setLayout(layout)

    def fetch_air_quality_ranking(self):
        try:
            ranking_data = self.api_client.fetch_air_quality_ranking()
            self.data = ranking_data.get('results', [])
            self.filtered_data = list(enumerate(self.data, start=1))  # 包含排名的初始数据
            if not self.data:
                QMessageBox.warning(self, "提示", "暂无城市空气质量排名数据！")
                self.table.setRowCount(0)  # 清空表格
                return

            self.update_table()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取空气质量排名数据失败: {e}")

    def update_table(self):
        # 更新表格显示
        self.table.setRowCount(len(self.filtered_data))
        for row, (rank, city_data) in enumerate(self.filtered_data):
            location = city_data.get('location', {})
            city_name = location.get('name', '暂无数据')
            path = location.get('path', '暂无数据')

            # 去掉重复的连续部分
            path_parts = path.split(',')
            processed_path = []
            for i, part in enumerate(path_parts):
                if i == 0 or part != path_parts[i - 1]:  # 只添加非重复部分
                    processed_path.append(part)
            processed_path = ', '.join(processed_path)

            aqi = city_data.get('aqi', '暂无数据')

            self.table.setItem(row, 0, QTableWidgetItem(str(rank)))  # 显示排名
            self.table.setItem(row, 1, QTableWidgetItem(city_name))
            self.table.setItem(row, 2, QTableWidgetItem(processed_path))  # 显示处理后的路径
            self.table.setItem(row, 3, QTableWidgetItem(str(aqi)))

    def filter_table(self):
        # 根据搜索框内容过滤数据，并保留排名信息
        query = self.search_box.text().strip().lower()
        self.filtered_data = [
            (rank, city) for rank, city in enumerate(self.data, start=1)
            if query in city.get('location', {}).get('name', '').lower()
        ]
        self.update_table()

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from utils.api_client import ApiClient

    app = QApplication(sys.argv)
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key

    window = AirQualityRanking(api_client)
    window.show()
    sys.exit(app.exec())
