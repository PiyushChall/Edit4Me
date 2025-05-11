from agent import GameAIAgent

def start_chat(api_key: str):
    agent = GameAIAgent(api_key)
    filename = "generated_game.py"
    print("🎮 Welcome to EditForMe a 2D Game AI Agent!")
    print("📝 Type 'new' to generate a new game, 'exit' to quit.")

    while True:
        command = input("\n💬 Your input: ")

        if command.strip().lower() == "exit":
            print("👋 Exiting...")
            break

        elif command.strip().lower() == "new":
            game_idea = input("🧠 Describe your 2D game idea: ")
            result = agent.handle_prompt(game_idea, filename)
            print(result)

        else:
            print("🔧 Applying your change to the existing game...")
            result = agent.handle_modification(command, filename)
            print(result)
