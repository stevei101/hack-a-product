from .tools.gemini import GeminiTool
from .tools.figma import FigmaTool

class OrchestrationService:
    """
    Service to orchestrate different tools.
    """
    def __init__(self):
        # In the future, this could dynamically load tools
        self.tools = {
            "gemini": GeminiTool(),
            "figma": FigmaTool()
        }

    async def process_request(self, tool_name: str, prompt: str) -> str:
        """
        Process a request by routing it to the specified tool.
        """
        tool = self.tools.get(tool_name)
        if not tool:
            return f"Tool '{tool_name}' not found."

        return await tool.execute(prompt)
