# Base response class
class Response:
    raw_response = None
    intent = None

    def __init__(self, raw_response):
        self.raw_response = raw_response

    def get_intent(self):
        return self.intent

    def process_values(self):
        raise NotImplementedError('Not yet implemented')

    def has_intent(self):
        if self.intent is None:
            return False
        return True
