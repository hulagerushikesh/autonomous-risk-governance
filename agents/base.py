from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def evaluate(self, input_data: dict) -> dict:
        pass

    @abstractmethod
    def report(self) -> dict:
        pass
