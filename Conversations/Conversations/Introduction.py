from App.Core.models import User
from Conversations.BaseComponents.BaseClasses import Conversation, UsesDataSource
from Conversations.BaseComponents.BaseClasses import EndOfConversation
from Conversations.BaseComponents.QuestionContext import Confirmation, AskForRepeat, QuestionContextBuilder
from Conversations.Questions.Introduction import AskForName, AskForSalutation
from helpers import debug


class Introduction(Conversation, UsesDataSource):
    required_properties = {
        'name': AskForName,
        'salutation': AskForSalutation,
    }

    def __init__(self):
        self.data_source = User()

    def start(self):
        # For each required property
        for (property, question_class) in self.required_properties.items():
            # Check if our data source has that property set
            if hasattr(self.data_source, property):
                data_source_attribute = getattr(self.data_source, property)
                # Check if that property has already been forfilled
                debug(data_source_attribute)
                if data_source_attribute == "":
                    return question_class()
            else:
                debug("Data source has no first name")
                continue
        return self.stop()

    def next_question(self):
        return self.start()

    def stop(self):
        return EndOfConversation(_("Your poppy is ready for use"))

    def get_intro_text(self):
        return "Hallo"

    def free_answer(self, question, response):

        for (property, question_class) in self.required_properties.items():
            if isinstance(question, question_class):
                if hasattr(response, 'text'):
                    method = getattr(self, 'set_' + property)
                    return method(response.text)
                else:
                    debug("Skip property")

    """ Set users salutation"""
    def intent_get_salutation(self, response):
        if hasattr(response, 'salutation'):
            salutation = response.salutation
        elif hasattr(response, 'contact'):
            salutation = response.contact
        elif hasattr(response, 'message_subject'):
            salutation = response.message_subject
        else:
            question_context = QuestionContextBuilder.new(
                type=AskForRepeat,
                current_question=AskForSalutation,
                next_question=None,
                intermediate_text=_("I am sorry, I didn't quite understand you. Could you please repeat that?")
            )
            return question_context

        return self.set_salutation(salutation=salutation)

    """ Use an intent to set the users name users name """
    def intent_get_name(self, response):
        if hasattr(response, 'contact'):
            name = response.contact
        else:
            name = response.text
        return self.set_name(name=name)

    """ Set the salutation of user """
    def set_salutation(self, salutation):
        self.data_source.salutation = salutation
        question_context = QuestionContextBuilder.new(
            type=Confirmation,
            current_question=AskForSalutation,
            next_question=self.next_question(),
            intermediate_text=_("From now on I'll address you with %s") % self.data_source.salutation
        )
        return question_context

    """ Set the users name """
    def set_name(self, name):
        self.data_source.name = name
        question_context = QuestionContextBuilder.new(
            type=Confirmation,
            current_question=AskForName,
            next_question=self.next_question(),
            intermediate_text=_("Goodday %s %s, it is a pleasure getting to know you")
                              % (self.data_source.salutation, name)
        )
        return question_context

