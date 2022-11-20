import requests


class WeaherProcessor:
    weather_token = "be8c48d3c55327e0c89e96c5a131a5e7"
    api_url = "https://api.openweathermap.org/data/2.5/weather?q={query}&appid={token}"

    def __init__(self, city, *args):
        self.city = city
        self.message: str

    def _get_weather_info(self):
        response = requests.get(self.api_url.format(query=self.city, token=self.weather_token))
        return response.json()

    def _create_response(self):
        data = self._get_weather_info()
        main = data.get("main")
        if main is None:
            self.message = "Город не найден"
            return

        temp = main["temp"] - 273.15
        feels_like = main["feels_like"] - 273.15
        pressure = main["pressure"]
        humidity = main["humidity"]

        return f"Температура в {self.city.title()} {round(temp)}°C, ощущается как {round(feels_like)}°C"\
            f"\nДавление: {pressure} мм рт. ст."\
            f"\nВлажность: {humidity}%"
        
    def run(self):
        self.message = self._create_response()

