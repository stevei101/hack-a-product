import os
import httpx
from .base import Tool

class FigmaTool(Tool):
    """
    A tool for interacting with the Figma API.
    """
    BASE_URL = "https://api.figma.com/v1/"

    def __init__(self):
        self.api_key = os.getenv("FIGMA_API_KEY")
        if not self.api_key:
            raise ValueError("FIGMA_API_KEY environment variable not set.")
        self.headers = {
            "X-Figma-Token": self.api_key,
        }

    async def execute(self, prompt: str) -> str:
        """
        Fetches details about a Figma file.
        The prompt should be the Figma file key.
        """
        file_key = prompt.strip()
        if not file_key:
            return "Error: Please provide a Figma file key as the prompt."

        url = f"{self.BASE_URL}files/{file_key}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()  # Raise an exception for bad status codes
                data = response.json()
                
                # Extract and return relevant information
                return f"Figma File Name: {data.get('name')}"

            except httpx.HTTPStatusError as e:
                return f"Error fetching Figma file: {e.response.status_code} - {e.response.text}"
            except Exception as e:
                return f"An unexpected error occurred: {e}"
