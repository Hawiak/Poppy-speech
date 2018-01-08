import Database.Database as db_instance

db_handler = db_instance.DatabaseHandler()
db = db_handler.get_db_instance()