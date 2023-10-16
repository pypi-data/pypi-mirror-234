from enum import StrEnum


class EntityType(StrEnum):
    
    HANDLER = "handler"
    STATE = "state"
    CALLBACK_DATA = "callback_data"
    KEYBOARD = "keyboard"
    MIDDLEWARE = "middleware"
    FILTER = "filter"
