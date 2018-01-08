import speech_recognition as sr

from App.Core.AppComponents import Singleton
from NLP import nlp
from helpers import debug, get_path


class IntentHandler(Singleton):

    context = None

    # Listen for user audio save it to a hardcoded file
    # @TODO change this to a more elegant way of saving
    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            debug("Say something!")
            audio = r.listen(source)

            # Write audio to a file which we will send to the API
            with open(get_path("/resources/audio/microphone-results.wav"), "wb") as f:
                f.write(audio.get_wav_data())

    # Get the intent from the NLP engine
    def get_intent(self):
        return nlp.get_intent("")

    # Format the raw response to a clean class
    def process_response(self, response):
        return nlp.process_response(response)

    # Listen for audio, process the audio and return a formatted response
    def wait_for_answer(self):
        self.listen()
        resp = self.get_intent()
        return self.process_response(resp)

    def listen_callback(self):
        print

    @staticmethod
    def get():
        return IntentHandler()

