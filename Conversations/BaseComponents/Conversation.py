from App.Core import intent_handler
from Conversations.BaseComponents.BaseClasses import EndOfConversation, Question, FreeAnswer
from Conversations.BaseComponents.QuestionContext import Confirmation, Success, AskForRepeat
from TTS import tts
from helpers import debug


class ConversationManager:

    conversation = None

    def get_conversation(self):
        debug("Getting conversation" + str(self.conversation))
        return self.conversation()


class ConversationListener:

    """ Listen for a response using the intent handler"""
    def listen(self):
        debug("Listening...")
        response = intent_handler.wait_for_answer()
        debug("Got response: " + str(response))
        return response


""" This class is responsible for fetching the right questions and firing off the intents on the conversation class """
class ConversationHandler:

    conversation = None
    question = None
    allow_free_answer = False

    def start(self, conversation):
        debug("Starting conversation: " + str(conversation))
        self.conversation = conversation
        if hasattr(self.conversation, 'get_intro_text'):
            tts.say(self.conversation.get_intro_text())
        return self.start_conversation()

    def start_conversation(self):
        end_of_conversation = False

        starting_question = self.conversation.start()

        if issubclass(starting_question.__class__, Question):
            self.question = QuestionHandler(starting_question)
        else:
            debug("Starting node is not of type question. Stopping conversation")
            return

        while end_of_conversation is False:
            self.question.ask()

            listener = ConversationListener()
            response = listener.listen()

            response_handler = ResponseHandler(response=response)
            if issubclass(self.question.question.__class__, FreeAnswer):
                response_handler.free_text_answer_allowed = True
            question_context = response_handler.get_question_context(
                conversation=self.conversation,
                current_question=self.question.question
            )

            if isinstance(question_context, Success):
                tts.say(question_context.intermediate_text)
                self.question.set(question=question_context.next_question)
            elif isinstance(question_context, AskForRepeat):
                self.question.set(question=question_context.current_question)
                self.question.repeat_question(True)
            elif isinstance(question_context, Confirmation):
                confirmation_result = response_handler.confirming_answer()
                if confirmation_result is True:
                    self.question.set(question=question_context.next_question)
                    tts.say(question_context.intermediate_text)
                elif confirmation_result is False:
                    self.question.set(question=question_context.current_question)

            if isinstance(self.question.question, EndOfConversation):
                debug("End of conversation")
                if self.question.question.text != "":
                    tts.say(self.question.question.text)
                end_of_conversation = True

        return True


""" Handle question logic """
class QuestionHandler:

    question = None
    is_repeat_question = False

    def __init__(self, question):
        self.question = question

    def set(self, question):
        self.question = question

    def ask(self):
        if self.is_repeat_question is True:
            tts.say(_("I'll repeat the question"))
            debug("Repeating question")
        question_text = self.question.ask_question()
        debug("Question: " + question_text)
        tts.say(question_text)

    def repeat_question(self, repeat):
        self.is_repeat_question = repeat


class ResponseHandler:
    response = None

    free_text_answer_allowed = False

    def __init__(self, response):
        self.set_response(response)

    def set_response(self, response):
        self.response = response

    def allow_free_text_answer(self):
        self.free_text_answer_allowed = True

    def confirming_answer(self):
        if hasattr(self.response, 'text'):
            tts.say(_("You've answered %s, is that right?") % self.response.text)
        confirmation_intent_response = intent_handler.wait_for_answer()
        if hasattr(confirmation_intent_response, 'intent'):
            if confirmation_intent_response.intent == 'confirmation_confirm':
                debug("Confirmed")
                return True
            elif confirmation_intent_response.intent == 'confirmation_deny':
                debug("Repeat question")
                tts.say(_("I'll repeat the question"))
                return False

    def get_question_context(self, conversation, current_question):
        question_context = None
        if self.response is None:
            debug("Response is not set")

        # Check if it has an intent
        debug(self.response.intent)
        if hasattr(self.response, 'intent') and self.response.intent is not None:
            conversation_intent_method = getattr(conversation, 'intent_' + self.response.intent)
            question_context = conversation_intent_method(response=self.response)
        else: # Does not have an intent
            debug("Intent is none")
            if self.free_text_answer_allowed is True:
                debug("Allow free text")
                if hasattr(conversation, 'free_answer'):
                    question_context = conversation.free_answer(question=current_question, response=self.response)
                else:
                    debug(conversation + " does not have free_answer method")

        if question_context is None:
            return False

        return question_context

