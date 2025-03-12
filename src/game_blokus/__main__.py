import os
from .game import BlokusGame

def main():
    # Clear screen and initialize game
    os.system('cls' if os.name == 'nt' else 'clear')
    game = BlokusGame()
    try:
        game.start_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Game state was not saved.")

if __name__ == "__main__":
    main()