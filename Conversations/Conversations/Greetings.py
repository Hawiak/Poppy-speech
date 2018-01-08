from Conversations.BaseComponents.BaseClasses import Conversation
from App.Core import user_manager


class Greetings(Conversation):
    user = None

    def __init__(self):
        self.user = user_manager.user

    def start(self):
        pass

    def stop(self):
        pass

    def get_intro_text(self):
        return _("Hello %s %s, welcome back!") % (self.user.salutation, self.user.name)

