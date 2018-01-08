import speech_recognition as sr
import time
from helpers import debug, to_camel_case
from TTS import tts
from NLP.Engines import api_key
from pony.orm import *


class CommandListener:

    command_centre = None

    def __init__(self):
        self.command_centre = CommandCentre()

    @db_session
    def callback(self, recognizer, audio):
        from App.Core import user_manager
        user_manager.get_user()
        debug("I heard something")
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            command = recognizer.recognize_wit(audio, api_key)
            debug("User said: " + command)
            aliasses = {'poepie', 'poppie', 'poppy', 'moppie', 'pappie'}

            for alias in aliasses:
                if str.lower(_("Hello") + alias) in str.lower(command).replace(" ", ""):
                    tts.say(_("Hello %s, what can I do for you?") % user_manager.user.name)
                    self.command_centre.start()

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def start(self):
        r = sr.Recognizer()
        m = sr.Microphone()
        r.pause_threshold = 0.2
        r.non_speaking_duration = 0.2
        with m as source:
            r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

        r.energy_threshold = 10

        # start listening in the background (note that we don't have to do this inside a `with` statement)
        stop_listening = r.listen_in_background(m, self.callback)
        # `stop_listening` is now a function that, when called, stops background listening

        # do some unrelated computations for 5 seconds
        for _ in range(50):
            time.sleep(0.1)  # we're still listening even though the main thread is doing other things

        # calling this function requests that the background listener stop listening
        # stop_listening(wait_for_stop=False)

        # do some more unrelated things
        while True:
            time.sleep(0.1)


class CommandCentre:

    def start(self):
        from App.Core import intent_handler
        response = intent_handler.wait_for_answer()
        if hasattr(response, 'intent'):
            if response.intent == 'get_day':
                from CommandCentre.commands import GetDay
                GetDay().execute()
            elif response.intent == 'get_weather':
                from CommandCentre.commands import GetWeather
                GetWeather().set_response(response).execute()
            else:
                debug("No intent found or something")


class Command:
    conversation = None

    def execute(self):
        raise NotImplementedError()


class RequiresResponse:
    response = None

    def set_response(self, response):
        self.response = response
        return self

    def execute(self):
        if self.response is None:
            raise Exception("No response is set")
