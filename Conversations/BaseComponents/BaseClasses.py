class Conversation:
    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def get_intro_text(self):
        raise NotImplementedError()

    def free_answer(self, question, response):
        raise NotImplementedError()


class UsesDataSource:
    data_source = None


class Question:
    def ask_question(self):
        raise NotImplementedError()

    def set_arg(self, name, value):
        setattr(self, name, value)


class FreeAnswer:
    pass


class ConfirmQuestion:
    def confirm_question(self, *args):
        raise NotImplementedError()


class Answer:

    def __init__(self):
        raise NotImplementedError()

    def handle(self, args=[]):
        raise NotImplementedError()

    def follow_up(self):
        pass


class Action:
    def trigger(self):
        raise NotImplementedError("Sub class of action must implement trigger method")


class EndOfConversation:

    text = ""

    def __init__(self, text):
        self.text = text