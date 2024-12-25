import sys

from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QWidget, QMessageBox, QGroupBox
)

from air_quality_class.air_quality_class_ui import AirQualityClass
from geo_class.geo_class_ui import GeoClass
from helper_class.helper_class_ui import HelperClass
from life_class.life_class_ui import LifestyleClass
from ocean_class.ocean_class_ui import OceanClass
from utils.api_client import ApiClient
from weather_class.weather_class_ui import WeatherClass


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SkyTracker")
        self.setFixedSize(500, 450)

        self.api_client = ApiClient()

        self.settings = QSettings("SkyTracker", "SkyTrackerApp")

        # 初始化 UI
        self.init_ui()

        self.check_saved_api_key()
        self.show_startup_message()

    def show_startup_message(self):
        startup_message = QMessageBox(self)
        startup_message.setIcon(QMessageBox.Icon.Information)
        startup_message.setWindowTitle("欢迎使用")
        startup_message.setText(
            "本程序数据源为心知天气，您需要拥有心知天气API Key才能使用本程序。\n\n"
            "请输入心知天气 API Key 并确认，解锁所有功能模块。\n\n"
            "提示：本程序功能基于心知天气试用版API，请确保您拥有试用版或更高级版本的API访问权限并拥有网络连接用于验证。"
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

        for button in [
            self.button_weather,
            self.button_air_quality,
            self.button_lifestyle,
            self.button_ocean,
            self.button_geo,
            self.button_helper
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

    def check_saved_api_key(self):
        saved_key = self.settings.value("api_key", "")
        if saved_key:
            self.input_key.setText(saved_key)
            self.verify_api_key(saved_key, show_message=False)

    def confirm_key(self):
        api_key = self.input_key.text().strip()
        if not api_key:
            QMessageBox.warning(self, "警告", "API Key 不能为空！")
            return

        self.verify_api_key(api_key)

    def verify_api_key(self, api_key, show_message=True):
        try:
            # 设置 API Key
            self.api_client.set_api_key(api_key)

            # 测试 API Key 是否有效
            if self.api_client.test_api_key():
                if show_message:
                    QMessageBox.information(self, "成功", "API Key 验证成功！")
                    self.ask_save_key(api_key)

                # 验证成功则启用所有按钮
                for button in [
                    self.button_weather,
                    self.button_air_quality,
                    self.button_lifestyle,
                    self.button_ocean,
                    self.button_geo,
                    self.button_helper
                ]:
                    button.setEnabled(True)
            else:
                if show_message:
                    QMessageBox.warning(self, "失败", "API Key 无效，请重新输入！")
        except Exception as e:
            if show_message:
                QMessageBox.critical(self, "错误", f"设置或验证 API Key 时出错: {e}")

    def ask_save_key(self, api_key):
        # 提示用户是否保存 API Key，下次启动免输入
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle("保存 API Key")
        msg_box.setText("是否要将当前验证成功的 API Key 保存？\n下次启动将自动使用，无需再次输入。")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        choice = msg_box.exec()

        if choice == QMessageBox.StandardButton.Yes:
            self.settings.setValue("api_key", api_key)
        else:
            self.settings.remove("api_key")

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
