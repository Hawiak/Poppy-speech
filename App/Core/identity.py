from App.Core.models import User
from pony.orm import *


class UserManager:
    user = None

    def get_user(self):
        try:
            self.user = User.select().order_by(desc(User.id)).first()
        except ObjectNotFound:
            pass

    def has_user(self):
        if self.user is not None:
            return True

        return False

