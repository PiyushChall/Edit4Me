from utils import read_code, write_code_to_file
import google.generativeai as genai
import os


class PythonAIAgent:  # Renamed class
    def __init__(self, api_key: str):
        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_code(self, user_prompt: str) -> str:  # Renamed method
        # Updated prompt string
        safe_prompt = f"Write a Python script for {user_prompt}. Avoid violence or unsafe content."
        response = self.model.generate_content(safe_prompt)

        if not response.parts:
            return "# Gemini did not return a response. The content may have been flagged by safety filters."

        return response.text

    def modify_code(self, change_prompt: str, filename: str = "generated_code.py") -> str:  # Renamed method and updated default filename
        existing_code = read_code(filename)
        if not existing_code:
            return "⚠️ No existing game code to modify."

        prompt = (  # Updated prompt string
            f"Here is a Python script:\n\n{existing_code}\n\n"
            f"Please update the code based on this user instruction:\n{change_prompt}.\n"
            "Avoid any unsafe or violent content."
        )
        response = self.model.generate_content(prompt)

        if not response.parts:
            return "# Gemini refused to respond. Try rephrasing your request."

        return response.text

    def handle_prompt(self, prompt: str, filename: str = "generated_code.py"):  # Updated default filename
        code = self.generate_code(prompt)  # Updated method call

        print("\n🔍 Generated Code Preview:\n" + "-" * 40)
        print(code)
        confirm = input("\n💬 Do you want to write this code to file? (yes/no): ").strip().lower()

        if confirm in ["yes", "y", "sure"]:
            return write_code_to_file(code, filename)
        else:
            return "❌ Code was not written to file."

    def handle_modification(self, change_prompt: str, filename: str = "generated_code.py"):  # Updated default filename
        code = self.modify_code(change_prompt, filename)  # Updated method call

        print("\n🔍 Updated Code Preview:\n" + "-" * 40)
        print(code)
        confirm = input("\n💬 Do you want to apply this change to the file? (yes/no): ").strip().lower()

        if confirm in ["yes", "y"]:
            return write_code_to_file(code, filename)
        else:
            return "❌ Modification was not saved."
