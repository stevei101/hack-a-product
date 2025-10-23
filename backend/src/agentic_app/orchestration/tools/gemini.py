import os
import google.generativeai as genai
from .base import Tool

class GeminiTool(Tool):
    """
    A tool for interacting with the Google Gemini API.
    """
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    async def execute(self, prompt: str) -> str:
        """
        Sends a prompt to the Gemini API and returns the response.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Handle potential API errors
            return f"An error occurred: {e}"
