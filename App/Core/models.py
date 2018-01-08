from Database import db
from pony import orm


class User(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Optional(str)
    salutation = orm.Optional(str)
