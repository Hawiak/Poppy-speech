import unittest
from faker import Faker
from pony import orm

from App import app
from App.App import App

from App.Core.models import User
from NLP.Engines.WitAI import WitAI
from TTS.engines import TtsGoogle

from Conversations.BaseComponents.QuestionContext import QuestionContextBuilder, QuestionContext
from Conversations.Questions.Introduction import AskForSalutation, AskForName


class TestAppMethods(unittest.TestCase):

    def test_app(self):
        self.assertIsInstance(app, App)

class TestUserCreation(unittest.TestCase):

    fake = None

    def setUp(self):
        self.fake = Faker()

    @orm.db_session
    def test_user_creation(self):
        name = self.fake.first_name()
        user = User()
        user.name = name

        self.assertEqual(user.name, name)
        orm.rollback()

    @orm.db_session
    def test_if_engine_is_creating(self):
        from NLP import nlp
        self.assertIsInstance(nlp, WitAI)
        orm.rollback()


    @orm.db_session
    def test_if_tts_is_creating(self):
        from TTS import tts
        self.assertIsInstance(tts, TtsGoogle)
        orm.rollback()

    def test_if_contextbuilder_returns_valid_object(self):
        current_question = AskForName()
        next_question = AskForSalutation
        intermediate_text = self.fake.text()
        context = QuestionContextBuilder.new(
            type=QuestionContext,
            current_question=current_question,
            next_question=next_question,
            intermediate_text=intermediate_text
        )

        self.assertIsInstance(context, QuestionContext)
        self.assertEqual(context.intermediate_text, intermediate_text)
        self.assertEqual(context.next_question, next_question)
        self.assertEqual(context.current_question, current_question)


if __name__ == '__main__':
    unittest.main()
