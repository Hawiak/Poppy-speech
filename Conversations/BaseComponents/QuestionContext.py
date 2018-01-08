class QuestionContext:

    current_question = None

    next_question = None

    intermediate_text = ""

    def set_next_question(self, next_question):
        self.next_question = next_question

    def set_intermediate_text(self, intermediate_text):
        self.intermediate_text = intermediate_text

    def set_current_question(self, current_question):
        self.current_question = current_question


class Confirmation(QuestionContext):
    pass


class Success(QuestionContext):
    pass


class AskForRepeat(QuestionContext):
    pass


class QuestionContextBuilder:
    @staticmethod
    def new(type, current_question, next_question, intermediate_text):
        context = type()
        context.set_current_question(current_question=current_question)
        context.set_next_question(next_question=next_question)
        context.set_intermediate_text(intermediate_text=intermediate_text)
        return context