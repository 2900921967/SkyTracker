import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox, QGroupBox
)
from utils.api_client import ApiClient
from weather_class.weather_class_ui import WeatherClass
from air_quality_class.air_quality_class_ui import AirQualityClass
from life_class.life_class_ui import LifestyleClass
from ocean_class.ocean_class_ui import OceanClass
from geo_class.geo_class_ui import GeoClass
from helper_class.helper_class_ui import HelperClass

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("天气查询系统")
        self.setFixedSize(500, 600)

        self.api_client = ApiClient()

        # 显示启动提示弹窗
        self.show_startup_message()

        self.init_ui()

    def show_startup_message(self):
        """显示启动提示弹窗"""
        startup_message = QMessageBox(self)
        startup_message.setIcon(QMessageBox.Icon.Information)
        startup_message.setWindowTitle("欢迎使用")
        startup_message.setText(
            "本程序基于心知天气API。\n\n请输入心知天气 API Key 并确认，解锁所有功能模块。\n\n提示：确保您有网络连接，API Key 可从心知天气官网获取。\n\n警告：本程序使用试用版API编写，如您使用的是免费版API并使用免费版API不支持的功能将会报错。"
        )
        startup_message.setStandardButtons(QMessageBox.StandardButton.Ok)
        startup_message.exec()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # API Key 输入框
        key_group = QGroupBox("API Key 设置")
        key_layout = QVBoxLayout()
        self.label_key = QLabel("请输入心知天气 API Key:")
        self.label_key.setStyleSheet("font-size: 14px;")
        self.input_key = QLineEdit()
        self.input_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_key.setPlaceholderText("在此输入您的 API Key")
        self.button_confirm = QPushButton("确认")
        self.button_confirm.clicked.connect(self.confirm_key)
        key_layout.addWidget(self.label_key)
        key_layout.addWidget(self.input_key)
        key_layout.addWidget(self.button_confirm)
        key_group.setLayout(key_layout)
        layout.addWidget(key_group)

        # 功能按钮区域
        function_group = QGroupBox("功能模块")
        function_layout = QVBoxLayout()

        self.button_weather = QPushButton("天气类功能")
        self.button_weather.setEnabled(False)
        self.button_weather.clicked.connect(self.open_weather_class)

        self.button_air_quality = QPushButton("空气类功能")
        self.button_air_quality.setEnabled(False)
        self.button_air_quality.clicked.connect(self.open_air_quality_class)

        self.button_lifestyle = QPushButton("生活类功能")
        self.button_lifestyle.setEnabled(False)
        self.button_lifestyle.clicked.connect(self.open_lifestyle_class)

        self.button_ocean = QPushButton("海洋类功能")
        self.button_ocean.setEnabled(False)
        self.button_ocean.clicked.connect(self.open_ocean_class)

        self.button_geo = QPushButton("地理类功能")
        self.button_geo.setEnabled(False)
        self.button_geo.clicked.connect(self.open_geo_class)

        self.button_helper = QPushButton("辅助类功能")
        self.button_helper.setEnabled(False)
        self.button_helper.clicked.connect(self.open_helper_class)

        # 添加按钮到布局
        for button in [
            self.button_weather, self.button_air_quality, self.button_lifestyle,
            self.button_ocean, self.button_geo, self.button_helper
        ]:
            button.setStyleSheet("font-size: 14px; padding: 10px;")
            function_layout.addWidget(button)

        function_group.setLayout(function_layout)
        layout.addWidget(function_group)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f7f7f7;
            }
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                margin-top: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 10px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                border: none;
            }
            QPushButton:disabled {
                background-color: #d3d3d3;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def confirm_key(self):
        """确认并验证 API Key"""
        api_key = self.input_key.text().strip()
        if not api_key:
            QMessageBox.warning(self, "警告", "API Key 不能为空！")
            return

        try:
            # 设置 API Key
            self.api_client.set_api_key(api_key)

            # 测试 API Key 是否有效
            if self.api_client.test_api_key():  # 假设 ApiClient 有此方法
                QMessageBox.information(self, "成功", "API Key 验证成功！")
                for button in [
                    self.button_weather, self.button_air_quality, self.button_lifestyle,
                    self.button_ocean, self.button_geo, self.button_helper
                ]:
                    button.setEnabled(True)
            else:
                QMessageBox.warning(self, "失败", "API Key 无效，请重新输入！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"设置或验证 API Key 时出错: {e}")

    def open_weather_class(self):
        self.weather_window = WeatherClass(self.api_client)
        self.weather_window.show()

    def open_air_quality_class(self):
        self.air_quality_window = AirQualityClass(self.api_client)
        self.air_quality_window.show()

    def open_lifestyle_class(self):
        self.lifestyle_window = LifestyleClass(self.api_client)
        self.lifestyle_window.show()

    def open_ocean_class(self):
        self.ocean_window = OceanClass(self.api_client)
        self.ocean_window.show()

    def open_geo_class(self):
        self.geo_window = GeoClass(self.api_client)
        self.geo_window.show()

    def open_helper_class(self):
        self.helper_window = HelperClass(self.api_client)
        self.helper_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
