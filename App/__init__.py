from App.App import App
import gettext
from config import USE_POPPY_LANGUAGE
from helpers import get_path
import locale

locale_path = get_path('/locale')
print("Locale path: " + locale_path)

lang = gettext.translation('poppy', localedir=locale_path, languages=[USE_POPPY_LANGUAGE])
lang.install()
locale.setlocale(locale.LC_ALL, USE_POPPY_LANGUAGE)

app = App()

