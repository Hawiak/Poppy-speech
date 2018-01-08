import os

from gtts import gTTS
from helpers import debug, get_path
from playsound import playsound


class Base:

    def say(self, text):
        raise NotImplemented('TTS engine is not implemented')

    def play_mp3_file(self, audio_file_path):
        playsound(audio_file_path)


class TtsGoogle(Base):

    """ Use text to prenounce a sentance with Google TTS.
    it will use the language defined in the USE_TTS_LANGUAGE language """
    def say(self, text):
        from config import USE_TTS_LANGUAGE

        # Fetch the fill path for the tts_result.mp3 in which the TTS results will be saved
        file_name = get_path('/resources/audio/tts_result.mp3')
        if os.path.isfile(file_name) is False:
            debug(str(file_name) + "File does not exists")
        tts = gTTS(text=str(text), lang=USE_TTS_LANGUAGE)
        tts.save(file_name)
        self.play_mp3_file(file_name)
