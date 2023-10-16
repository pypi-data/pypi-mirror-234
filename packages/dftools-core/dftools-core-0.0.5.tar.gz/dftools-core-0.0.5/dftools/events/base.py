
from enum import Enum

class EventLevel(int, Enum):
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    EXTENDED_INFO = 15
    DEBUG = 10
    TEST = 5

class BaseEvent():
    
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)
    
    def level(self) -> EventLevel:
        return EventLevel.DEBUG

    def message(self) -> str:
        raise Exception("message() not implemented for event")

    def code(self) -> str:
        raise Exception("code() not implemented for event")
    
class TestLevel(BaseEvent):
    def level(self) -> EventLevel:
        return EventLevel.TEST
    
class DebugLevel(BaseEvent):
    def level(self) -> EventLevel:
        return EventLevel.DEBUG

class ExtendedInfoLevel(BaseEvent):
    def level(self) -> EventLevel:
        return EventLevel.EXTENDED_INFO
    
class InfoLevel(BaseEvent):
    def level(self) -> EventLevel:
        return EventLevel.INFO

class WarnLevel(BaseEvent):
    def level(self) -> EventLevel:
        return EventLevel.WARN

class ErrorLevel(BaseEvent):
    def level(self) -> EventLevel:
        return EventLevel.ERROR


## Standard events with message provided using the argument msg only

class StandardEvent(BaseEvent):
    def __init__(self, msg : str) -> None:
        self.msg = msg

    def code(self):
        return "A-000"

    def message(self):
        return f"{self.msg}"
    
class StandardTestEvent(StandardEvent):
    def level(self) -> EventLevel:
        return EventLevel.TEST

class StandardDebugEvent(StandardEvent):
    def level(self) -> EventLevel:
        return EventLevel.DEBUG
    
class StandardInfoEvent(StandardEvent):
    def level(self) -> EventLevel:
        return EventLevel.INFO

class StandardExtendedInfoEvent(StandardEvent):
    def level(self) -> EventLevel:
        return EventLevel.EXTENDED_INFO

class StandardErrorEvent(StandardEvent):
    def level(self) -> EventLevel:
        return EventLevel.ERROR
