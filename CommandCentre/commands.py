from CommandCentre.components import Command, RequiresResponse
from TTS import tts
from Weather import weather
import math
import datetime


class GetDay(Command):
    def execute(self):
        now = datetime.datetime.now()
        tts.say(_("Today is %s") % now.strftime("%A %d %b"))


class GetWeather(Command, RequiresResponse):
    def execute(self):
        weather.set_location(self.response.location)
        current_weather = weather.get_current_weather()
        temp = current_weather.get_temperature('celsius')
        tts.say("Het wordt vandaag %s en %s graden in %s" % (current_weather.get_detailed_status(), math.floor(temp['temp_max']),
                                                             self.response.location, ))

