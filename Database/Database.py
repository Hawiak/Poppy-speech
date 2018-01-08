from pony import orm


class DatabaseHandler:

    db = None

    def __init__(self):
        self.db = orm.Database()
        self.db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

    def get_db_instance(self):
        return self.db
