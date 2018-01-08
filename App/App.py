from pony.orm import db_session
from Conversations.BaseComponents import conversation_manager, conversation_handler
from Conversations.Conversations import Greetings, Introduction
from Database import db
from PSM import psm
from PSM.States import StandBy
from helpers import debug
from .Core import user_manager
from .Core.AppComponents import Singleton
from CommandCentre.components import CommandListener


class App(Singleton):

    """
    This will ensure the tables are generated, migrations are not supported as of the moment but will
    be available at a later moment
    """
    def __init__(self):

        db.generate_mapping(create_tables=True)

    """ 
    Start the app in Pony's DB SESSION wrapper this will enable usage of the database during the apps runtime 
    """
    @db_session
    def start(self):

        # Sit up robot whenever available
        psm.go_to_state(StandBy())

        # Try and get the user from the user manager
        user_manager.get_user()

        # When user is available, we'll greet the user, otherwise start introduction
        if user_manager.has_user() is True:
            debug("Has a user")
            conversation_manager.conversation = Greetings.Greetings
        else:
            debug("Does not have a user")
            conversation_manager.conversation = Introduction.Introduction

        # Get the conversation handler
        conversation = conversation_manager.get_conversation()

        # Start the conversation
        conversation_handler.start(conversation)

        # Commit changes to prevent data loss whilst listening to the user in the commandcentre
        db.commit()

        command_listener = CommandListener()
        command_listener.start()

        # Commit changes to the database
        db.commit()
