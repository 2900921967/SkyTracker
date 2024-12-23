# SkyTracker

## 项目简介

本项目是一个基于心知天气 API 的桌面应用程序，提供天气、空气质量、生活指数、地理信息等多种查询功能，帮助用户快速了解所需的气象信息。

---

## 功能模块

- **天气类**
    - 天气实况
    - 逐日天气预报
    - 24 小时逐小时天气预报
    - 24 小时历史天气
    - 气象灾害预警

- **空气类**
    - 空气质量实况
    - 空气质量城市排行
    - 24 小时空气质量历史
    - 逐日空气质量预报
    - 逐小时空气质量预报

- **生活类**
    - 生活指数
    - 农历节气生肖
    - 机动车尾号限行

- **海洋类**
    - 逐小时潮汐预报

- **地理类**
    - 日出日落
    - 月出月落与月相

- **辅助类**
    - 城市搜索

---

## 项目依赖

- Python >= 3.8
- PyQt6
- requests

---

## 使用方法

1. 启动Main程序后，在主界面输入您的心知天气 API Key。
2. 点击确认后，选择对应的功能模块进入查询。
3. 在功能模块内按照提示输入城市或其他信息进行查询。

---

## 心知天气 API

本项目使用 [心知天气 API](https://www.seniverse.com/) 提供的气象数据，您需要申请自己的 API Key 才能正常运行。

---

## 许可证

本项目采用 [MIT 开源许可证](LICENSE)。