import requests

class ApiClient:
    def __init__(self):
        self.api_key = None
        self.base_url = "https://api.seniverse.com/v3"

    def set_api_key(self, api_key):
        """设置 API Key"""
        self.api_key = api_key

    def test_api_key(self):
        """验证 API Key 是否有效"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        try:
            # 测试请求示例：获取一个默认位置的当前天气
            endpoint = f"{self.base_url}/weather/now.json"
            params = {
                "key": self.api_key,
                "location": "beijing",  # 使用一个默认位置
                "language": "zh-Hans",
                "unit": "c",
            }

            response = requests.get(endpoint, params=params)
            response.raise_for_status()

            # 检查返回数据是否包含预期的 "results" 字段
            data = response.json()
            if "results" in data and data["results"]:
                return True  # API Key 验证成功
            return False  # 数据结构不匹配，可能无效
        except requests.exceptions.RequestException as e:
            print(f"API Key 验证失败: {e}")
            return False

    def fetch_current_weather(self, location, language="zh-Hans", unit="c"):
        """获取天气实况数据"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        endpoint = f"{self.base_url}/weather/now.json"
        params = {
            "key": self.api_key,
            "location": location,
            "language": language,
            "unit": unit,
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_daily_forecast(self, location, days=5, language="zh-Hans", unit="c", start=0):
        """获取逐日天气预报数据"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        endpoint = f"{self.base_url}/weather/daily.json"
        params = {
            "key": self.api_key,
            "location": location,
            "language": language,
            "unit": unit,
            "start": start,
            "days": days,
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_hourly_forecast(self, location, hours=24, language="zh-Hans", unit="c", start=0):
        """获取逐小时天气预报数据"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        endpoint = f"{self.base_url}/weather/hourly.json"
        params = {
            "key": self.api_key,
            "location": location,
            "language": language,
            "unit": unit,
            "start": start,
            "hours": hours,
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_hourly_history(self, location, language="zh-Hans", unit="c"):
        """获取过去24小时历史天气数据"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        endpoint = f"{self.base_url}/weather/hourly_history.json"
        params = {
            "key": self.api_key,
            "location": location,
            "language": language,
            "unit": unit,
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_weather_alerts(self, location, detail="more"):
        """获取气象灾害预警数据"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        endpoint = f"{self.base_url}/weather/alarm.json"
        params = {
            "key": self.api_key,
            "location": location,
            "detail": detail,
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_current_air_quality(self, location, language="zh-Hans", scope="city"):
        """获取空气质量实况数据"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        endpoint = f"{self.base_url}/air/now.json"
        params = {
            "key": self.api_key,
            "location": location,
            "language": language,
            "scope": scope,
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_air_quality_ranking(self, language="zh-Hans"):
        """获取空气质量城市排名数据"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        endpoint = f"{self.base_url}/air/ranking.json"
        params = {
            "key": self.api_key,
            "language": language,
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_hourly_air_quality(self, location, language="zh-Hans", scope="city"):
        """获取过去24小时空气质量历史数据"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        endpoint = f"{self.base_url}/air/hourly_history.json"
        params = {
            "key": self.api_key,
            "location": location,
            "language": language,
            "scope": scope,
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_daily_air_quality(self, location, language="zh-Hans"):
        """获取逐日空气质量预报数据"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        endpoint = f"{self.base_url}/air/daily.json"
        params = {
            "key": self.api_key,
            "location": location,
            "language": language,
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_hourly_air_quality_forecast(self, location, language="zh-Hans"):
        """获取逐小时空气质量预报数据"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        endpoint = f"{self.base_url}/air/hourly.json"
        params = {
            "key": self.api_key,
            "location": location,
            "language": language,
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_lifestyle_index(self, location, language="zh-Hans", days=1):
        """获取生活指数数据"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        endpoint = f"{self.base_url}/life/suggestion.json"
        params = {
            "key": self.api_key,
            "location": location,
            "language": language,
            "days": days,
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        result = response.json()

        # 提取 results 数据
        results = result.get('results', [])
        if not results:
            raise ValueError("API 响应中无结果数据")

        # 获取 suggestion 列表
        suggestion_list = results[0].get('suggestion', [])
        if not suggestion_list or not isinstance(suggestion_list, list):
            raise ValueError("suggestion 数据格式不正确")

        # 返回 suggestion 列表的第一个元素
        first_suggestion = suggestion_list[0]
        if not isinstance(first_suggestion, dict):
            raise ValueError("第一天的生活指数数据格式不正确")

        return first_suggestion

    def fetch_lunar_calendar(self, start=0, days=1):
        """获取农历节气生肖数据"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        endpoint = f"{self.base_url}/life/chinese_calendar.json"
        params = {
            "key": self.api_key,
            "start": start,
            "days": days,
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        result = response.json()

        # 提取 chinese_calendar 数据
        chinese_calendar = result.get('results', {}).get('chinese_calendar', [])
        if not chinese_calendar:
            raise ValueError("No chinese_calendar data found")

        return chinese_calendar[0]  # 返回第一天的数据

    def fetch_vehicle_restriction(self, location):
        """获取机动车尾号限行数据"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        endpoint = f"{self.base_url}/life/driving_restriction.json"
        params = {
            "key": self.api_key,
            "location": location,
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        result = response.json()

        results = result.get('results', [{}])
        if not results:
            raise ValueError("No vehicle restriction data found")

        return results[0]  # 返回第一条数据

    def fetch_tides_forecast(self, port):
        """获取逐小时潮汐预报数据"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        endpoint = f"{self.base_url}/tide/daily.json"
        params = {
            "key": self.api_key,
            "port": port,
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        result = response.json()

        # 提取潮汐数据
        results = result.get('results', [{}])
        if not results:
            raise ValueError("No tide data found")

        return results[0]  # 返回第一条数据

    def fetch_sun_times(self, location, days=1, language="zh-Hans", start=0):
        """获取日出日落时间数据"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        endpoint = f"{self.base_url}/geo/sun.json"
        params = {
            "key": self.api_key,
            "location": location,
            "language": language,
            "start": start,
            "days": days,
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        result = response.json()

        # 提取 sun 数据
        results = result.get('results', [{}])
        if not results:
            raise ValueError("No sun times data found")

        return results[0]  # 返回第一条数据

    def fetch_moon_times(self, location, days=1, language="zh-Hans", start=0):
        """获取月出月落和月相数据"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        endpoint = f"{self.base_url}/geo/moon.json"
        params = {
            "key": self.api_key,
            "location": location,
            "language": language,
            "start": start,
            "days": days,
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        result = response.json()

        # 提取 moon 数据
        results = result.get('results', [{}])
        if not results:
            raise ValueError("No moon times data found")

        return results[0]  # 返回第一条数据

    def search_city(self, query):
        """搜索城市"""
        if not self.api_key:
            raise RuntimeError("API Key 未设置！")

        endpoint = f"{self.base_url}/location/search.json"
        params = {
            "key": self.api_key,
            "q": query,
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    api_client = ApiClient()
    api_client.set_api_key("your_api_key_here")  # 替换为实际的 API Key
    try:
        result = api_client.fetch_lifestyle_index(location="shanghai")
        print(result)
    except Exception as e:
        print(f"Error: {e}")
