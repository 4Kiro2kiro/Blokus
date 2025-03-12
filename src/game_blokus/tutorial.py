from .utils import clear_screen

def start_tutorial(game):
    """Tutorial menu with section choices"""
    while True:
        clear_screen()
        print("\n--- Blokus Tutorial ---")
        print("Choose a section to explore:")
        print("1. Game Rules")
        print("2. Strategy Tips")
        print("3. Program Usage and Interface")
        print("4. Return to Main Menu")

        choice = input("\nEnter your choice (1-4): ")
        if choice == '1':
            show_rules()
        elif choice == '2':
            show_strategies()
        elif choice == '3':
            show_interface()
        elif choice == '4':
            print("\nReturning to main menu...")
            clear_screen()
            return game.start_game()
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
            input("Press Enter to continue...")

def show_rules():
    """Displays the game rules"""
    print("\n--- Game Rules ---")
    print("1. Each player starts with a set of uniquely shaped pieces.")
    print("2. Players take turns placing one piece on the board.")
    print("3. Each piece must touch another piece of the same color at a corner but must not share an edge.")
    print("4. The first piece of each player must touch a corner of the board.")
    print("5. The goal is to place as many of your pieces on the board as possible.")
    print("6. The game ends when no player can place any more pieces.")
    print("7. The player with the fewest squares left unplaced wins.")
    input("\nPress Enter to return to the tutorial menu.")

def show_strategies():
    """Displays strategy tips for the game"""
    print("\n--- Strategy Tips ---")
    print("1. Place larger pieces early: Using bigger pieces at the beginning gives you more options later and let you win more points.")
    print("2. Control the middle: Focus on controlling the middle of the board to increase your placement options.")
    print("3. Block your opponents: Strategically place your pieces to limit the moves of other players.")
    print("4. Save versatile pieces: Keep a few small or flexible pieces for the endgame to fit into tight spaces.")
    print("5. Observe your opponents: Pay attention to where other players are placing their pieces to anticipate and counter their moves.")
    input("\nPress Enter to return to the tutorial menu.")

def show_interface():
    """Displays an explanation of the game interface and controls"""
    print("\n--- Program Usage and Interface ---")
    print("1. Game Board: The main game board displays the grid where players place their pieces.")
    print("   - Each player's color is represented, helping to distinguish pieces.")
    print("   - Corners and edges guide placement, showing where pieces can fit.")
    print("2. Player Area: Each player has an area showing their available pieces.")
    print("   - Pieces are numbered to make selection easy.")
    print("   - When a piece is used, it’s removed from the list.")
    print("3. Controls:")
    print("   - Enter the piece number to select it and see placement options.")
    print("   - Press 's' to save the game at any time.")
    print("   - Press 'l' to load a previously saved game.")
    print("   - Press 'q' to quit the game.")
    print("4. Piece Placement:")
    print("   - After selecting a piece, you’ll enter coordinates (x, y) for its placement.")
    print("   - You can rotate the piece by entering a rotation value (0-3).")
    print("   - Optionally, you can flip the piece to fit tight spaces.")
    print("\nThis section covers all the essentials to navigate and control the game.")
    input("\nPress Enter to return to the tutorial menu.")
