from agent import PythonAIAgent  # Changed import

def start_chat(api_key: str):
    agent = PythonAIAgent(api_key)  # Changed class instantiation
    filename = "generated_code.py"  # Changed default filename
    # Changed welcome message
    print("🐍 Welcome to EditForMe - Your Python AI Code Assistant!")
    # Note: The next line still refers to 'game' but instructions didn't specify changing it.
    # If this needs to change, a new instruction would be required.
    print("📝 Type 'new' to generate a new game, 'exit' to quit.")

    while True:
        command = input("\n💬 Your input: ")

        if command.strip().lower() == "exit":
            print("👋 Exiting...")
            break

        elif command.strip().lower() == "new":
            # Changed input prompt
            game_idea = input("📝 What Python script would you like to generate? ")
            result = agent.handle_prompt(game_idea, filename)
            print(result)

        else:
            # Changed message
            print("🔧 Applying your change to the existing code...")
            result = agent.handle_modification(command, filename)
            print(result)
