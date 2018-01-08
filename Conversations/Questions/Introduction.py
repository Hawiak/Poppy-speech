from Conversations.BaseComponents.BaseClasses import Question, FreeAnswer


class AskForName(Question, FreeAnswer):

    def ask_question(self):
        return _("What is your complete name?")


class AskForSalutation(Question, FreeAnswer):

    def ask_question(self):
        return _("How do you wish to be addressed?")

