import os
import time
from .utils import clear_screen


def main_menu(game):
        """
        Retourne au menu principal du jeu.
        
        Args:
            game (BlokusGame): L'instance du jeu Blokus.
        """
        input()
        clear_screen()
        game.start_game()
        
def start_spectator(game):
    """
    Launch a spectator mode where two AI players compete against each other, each controlling two colors.
    """
    print("\n🕶️ Spectator Mode Activated: AI Duel 🕶️")

    valid_levels = ["easy", "medium", "hard"]
    ai_levels = []

    for i in range(2):
        while True:
            ai_level = input(f"Select difficulty level for AI {i + 1} (easy/medium/hard): ").lower()
            if ai_level in valid_levels:
                ai_levels.append(ai_level)
                ai_levels.append(ai_level)  # Chaque IA contrôle deux couleurs
                break
            else:
                print("Invalid choice. Please enter 'easy', 'medium', or 'hard'.")

    def get_valid_ai_speed(prompt="Select the speed of the AI (seconds between moves, value between 0 and 10): "):
        while True:
            try:
                ai_speed = int(input(prompt))
                if 0 <= ai_speed <= 10:
                    return ai_speed
                else:
                    print("Invalid choice. Please enter an integer between 0 and 10.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    ai_speed = get_valid_ai_speed()
    game.reset_game(num_players=4, ai_levels=ai_levels)
    
    print("\nThe AIs are preparing to play...")
    time.sleep(1)

    game_over = False
    while not game_over:
        clear_screen()
        game.board.display()

        current_player = game.players[game.current_player]
        print(f"\nAI {current_player.color} ({current_player.level}) is thinking...")

        # Vérifier si le joueur actuel peut jouer
        can_play = any(
            game.board.find_valid_moves(variant, current_player.color)
            for piece_id in current_player.remaining_pieces
            for piece in [current_player.pieces[piece_id]]
            for variant in piece.get_all_variations()
        )

        if can_play:
            current_player.play(game.board)
            time.sleep(int(ai_speed))
        
        game.current_player = (game.current_player + 1) % len(game.players)

        # Vérifier si la partie est terminée
        game_over = all(
            not any(
                game.board.find_valid_moves(variant, player.color)
                for piece_id in player.remaining_pieces
                for piece in [player.pieces[piece_id]]
                for variant in piece.get_all_variations()
            )
            for player in game.players
        )

    clear_screen()
    game.board.display()
    
    # Calcul des scores pour chaque IA
    ai_scores = [0, 0]
    ai_squares_placed = [0, 0]
    ai_squares_remaining = [0, 0]

    for i, player in enumerate(game.players):
        squares_remaining = sum(
            sum(sum(row) for row in player.pieces[piece_id].shape)
            for piece_id in player.remaining_pieces
        )
        squares_placed = sum(
            sum(sum(row) for row in player.pieces[j].shape)
            for j in range(len(player.pieces))
            if j not in player.remaining_pieces
        )
        final_score = squares_placed - squares_remaining
        ai_index = i // 2  # Chaque IA contrôle deux joueurs
        ai_scores[ai_index] += final_score
        ai_squares_placed[ai_index] += squares_placed
        ai_squares_remaining[ai_index] += squares_remaining

    # Affichage des scores finaux pour les IA
    print("\n🏆 Game Over! 🏆\n")
    print("Final Scores:\n")
    for i in range(2):
        print(f"AI {i + 1}:")
        print(f"  {'🥇' if ai_scores[i] == max(ai_scores) else '🥈'} Final Score: {ai_scores[i]}")
        print(f"   🟩 Squares placed: +{ai_squares_placed[i]}")
        print(f"   🟥 Remaining squares: -{ai_squares_remaining[i]}")
        print("=" * 40 + "\n")

    print("\n🎉 Spectator Mode Finished! 🎉")
    input("Press Enter to return to the main menu.")
    main_menu(game)

