import argparse
from chatbot import start_chat


def main():
    parser = argparse.ArgumentParser(description="AI 2D Game Code Generator")
    parser.add_argument("--api_key", type=str, required=True, help="Gemini API Key")
    parser.add_argument("--chat", action="store_true", help="Run in interactive chat mode")
    args = parser.parse_args()

    if args.chat:
        start_chat(args.api_key)


if __name__ == "__main__":
    main()

'''
To run this AI:
1. Open terminal where this code is present and type: "python main.py --api_key=YOUR_API_KEY --chat"
2. Replace YOUR_API_KEY with GOOGLE_API_KEY you have (If you dont have you can use this api_key : "AIzaSyDWU96YGaNJWcsuRx9tcwHGTbAHTGv4UFc" temporarily. This key will be deleted in 3 days)
3. Now a chat interface will open where you can prompt your game detail to the AI and the AI will bring your game idea into reality.
4. Now the agent would ask if he should implement the changes in the code: type "yes" to implement and "no" to discard the changes.
5. You can also continue the chat after the game-code has been created to make changes in your game. 
6. You will have to delete the beginning and the end of the generated code to execute it properly
'''