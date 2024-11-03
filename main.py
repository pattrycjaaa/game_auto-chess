# main.py

"""
main.py

The entry point of the application where the game flow is orchestrated.
Includes the main function to play the game rounds.
"""

from shop import buy_units
from ai_player import AIPlayer
from game_logic import battle_round, check_victory, plot_damage_stats, display_unit_health
from utils import total_health
import traceback

def play_game_round(max_rounds=5):
    """
    Main function to play the game.
    """
    try:
        budget = 20  # Starting budget for the player
        player_units = buy_units(budget)

        # AI Opponent
        ai_budget = 20
        ai_player = AIPlayer(ai_budget)
        opponent_units = ai_player.units

        round_number = 1
        while round_number <= max_rounds:
            print(f"\n--- Round {round_number} ---")
            battle_round(player_units, opponent_units)

            # Display health after each round
            display_unit_health(player_units, opponent_units)

            result = check_victory(player_units, opponent_units)
            if result:
                print(f"\n{result}")
                break

            round_number += 1

        # Check victory based on remaining health if max rounds reached
        if not result:
            player_health = total_health(player_units)
            opponent_health = total_health(opponent_units)
            if player_health > opponent_health:
                result = "Player wins by remaining health!"
            elif opponent_health > player_health:
                result = "Opponent wins by remaining health!"
            else:
                result = "Draw by equal remaining health!"

            print(f"\n{result}")

        # Display damage statistics
        plot_damage_stats(player_units, opponent_units)

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    # Run the game
    play_game_round(max_rounds=5)
