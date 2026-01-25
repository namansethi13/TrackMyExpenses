from abc import ABC, abstractmethod

class BaseChatInterface(ABC):
    @abstractmethod
    def to_incoming_event(self, payload: dict):
        pass