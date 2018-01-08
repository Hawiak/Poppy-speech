import configparser
import os.path
import os


class nlpEngineBase:
    def get_intent(self, text):
        raise NotImplemented('NLP engine is not implemented')