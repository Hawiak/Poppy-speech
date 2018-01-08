import pyowm
from helpers import debug, get_path
import configparser
from config import USE_TTS_LANGUAGE

config = configparser.ConfigParser()
config_path = get_path("Weather/weather.config")
config.read(config_path)


class UsesApiKey:
    api_key = None


class BaseWeatherProvider:
    location = None

    def get_current_weather(self):
        raise NotImplementedError()

    def set_location(self, location):
        self.location = location


class OpenWeatherMap(UsesApiKey, BaseWeatherProvider):

    client = None

    weather = None

    def __init__(self):
        self.api_key = config.get('openweathermap_api', 'key')
        self.client = pyowm.OWM(self.api_key, language=USE_TTS_LANGUAGE)

    def get_current_weather(self):
        if self.location is not None:
            observation = self.client.weather_at_place(self.location)
            self.weather = observation.get_weather()
        else:
            debug("Location is not set, set location before calling this method")
        return self.weather



