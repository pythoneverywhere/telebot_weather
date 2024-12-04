import requests

class WeatherService:
    def __init__(self):
        self.api_url = "https://api.weather.yandex.ru/v2/informers"
        self.api_key = "e1b1140c-fff6-43dc-aa2b-bc59e620c89e"

    def get_weather(self, lat: float, lon: float):
        
        headers = {
            "X-Yandex-API-Key": self.api_key
        }

        response = requests.get(f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}', headers=headers)

        if response.status_code == 200:
            data = response.json()
            return {
                "temp": data["fact"]["temp"],
                "condition": data["fact"]["condition"],
                "feels_like": data["fact"]["feels_like"]
            }
        else:
            response.raise_for_status()
