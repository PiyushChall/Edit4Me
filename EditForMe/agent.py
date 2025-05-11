from utils import read_code, write_code_to_file
import google.generativeai as genai
import os


class GameAIAgent:
    def __init__(self, api_key: str):
        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_game_code(self, user_prompt: str) -> str:
        safe_prompt = f"Write a Python script for a 2D top-down game. {user_prompt}. Avoid violence or unsafe content."
        response = self.model.generate_content(safe_prompt)

        if not response.parts:
            return "# Gemini did not return a response. The content may have been flagged by safety filters."

        return response.text

    def modify_game_code(self, change_prompt: str, filename: str = "generated_game.py") -> str:
        existing_code = read_code(filename)
        if not existing_code:
            return "⚠️ No existing game code to modify."

        prompt = (
            f"Here is a Python script for a 2D game:\n\n{existing_code}\n\n"
            f"Please update the code based on this user instruction:\n{change_prompt}.\n"
            "Avoid any unsafe or violent content."
        )
        response = self.model.generate_content(prompt)

        if not response.parts:
            return "# Gemini refused to respond. Try rephrasing your request."

        return response.text

    def handle_prompt(self, prompt: str, filename: str = "generated_game.py"):
        code = self.generate_game_code(prompt)

        print("\n🔍 Generated Code Preview:\n" + "-" * 40)
        print(code)
        confirm = input("\n💬 Do you want to write this code to file? (yes/no): ").strip().lower()

        if confirm in ["yes", "y", "sure"]:
            return write_code_to_file(code, filename)
        else:
            return "❌ Code was not written to file."

    def handle_modification(self, change_prompt: str, filename: str = "generated_game.py"):
        code = self.modify_game_code(change_prompt, filename)

        print("\n🔍 Updated Code Preview:\n" + "-" * 40)
        print(code)
        confirm = input("\n💬 Do you want to apply this change to the file? (yes/no): ").strip().lower()

        if confirm in ["yes", "y"]:
            return write_code_to_file(code, filename)
        else:
            return "❌ Modification was not saved."
