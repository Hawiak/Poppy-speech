from NLP.nlpEngineBase import nlpEngineBase
from wit import Wit
from NLP.Engines.components import Response
from helpers import debug, get_path
from NLP.Engines import api_key


class WitAI(nlpEngineBase):

    def get_intent(self, audio_path):
        # Create the API client
        client = Wit(api_key)

        # Send the .wav file we've created earlier to the API
        try:
            with open(get_path('/resources/audio/microphone-results.wav'), 'rb') as f:
                resp = client.speech(f, None, {'Content-Type': 'audio/wav'})
                return resp
        except:
            debug("Microphone-results failed to open")

    def process_response(self, raw_response):
        response = WitResponse(raw_response)
        response.process_values()
        return response


class WitResponse(Response):
    intent_confidence = 0
    text = ""

    def process_values(self):
        if self.raw_response:
            self.text = self.raw_response['_text']
            debug(self.raw_response)
            for (label, value) in self.raw_response['entities'].items():
                if label == 'intent':
                    self.intent = value[0]['value']
                    self.intent_confidence = value[0]['confidence'] * 100
                else:
                    setattr(self, label, value[0]['value'])