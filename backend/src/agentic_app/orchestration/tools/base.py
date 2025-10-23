from abc import ABC, abstractmethod

class Tool(ABC):
    """
    Abstract base class for a generic tool.
    """
    @abstractmethod
    async def execute(self, prompt: str) -> str:
        """
        Execute the tool with a given prompt and return the result.
        """
        pass
