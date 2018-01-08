from config import USE_NLP_LANGUAGE
from helpers import get_path
import configparser

config = configparser.ConfigParser()
config_path = get_path("NLP/nlp.config")
config.read(config_path)
_api_key_name = 'nlp_api_' + USE_NLP_LANGUAGE
api_key = config.get(_api_key_name, 'wit')
