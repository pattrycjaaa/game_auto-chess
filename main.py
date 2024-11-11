# main.py

from shop import buy_units
from game_logic import battle_round, check_victory, plot_damage_stats, display_unit_health
from utils import apply_initial_faction_buffs
from player import Player
import traceback

def play_game_round(max_rounds=5):
    """
    Main function to play the game.
    """
    try:
        player1 = Player(name="Player 1")
        player2 = Player(name="Player 2")

        # Player 1 buys units
        print("Player 1, build your army!")
        player1_units, player1.budget = buy_units(player1.budget, player_number=1, player_units=None)

        # Player 2 buys units
        print("\nPlayer 2, build your army!")
        player2_units, player2.budget = buy_units(player2.budget, player_number=2, player_units=None)

        # Apply initial faction buffs
        apply_initial_faction_buffs(player1_units)
        apply_initial_faction_buffs(player2_units)

        round_number = 1
        while round_number <= max_rounds:
            print(f"\n--- Round {round_number} ---")
            print("Please enter the numbers of ALL your units in the order you want them to be attacked (separated by commas).")
            print("Or enter 'd' for default order.")
            for i, unit in enumerate(player1_units, start=1):
                print(f"{i}: {unit.name} (Health: {unit.health}, Attack: {unit.attack})")
            
            while True:
                try:
                    order_input = input("Enter ALL unit numbers in order (e.g. 1,2,3) or 'd' for default: ")
                    if order_input.lower() == 'd':
                        player1_attack_order = player1_units[:]
                        break
                    order = order_input.split(",")
                    if len(order) != len(player1_units):
                        print(f"Error: You must specify all {len(player1_units)} units.")
                        continue
                    if sorted([int(x) for x in order]) != list(range(1, len(player1_units) + 1)):
                        print("Error: You must use each number exactly once.")
                        continue
                    player1_attack_order = [player1_units[int(num)-1] for num in order]
                    break
                except (ValueError, IndexError):
                    print("Error: Invalid input. Use format like 1,2,3")

            print("Selected order:")
            for unit in player1_attack_order:
                print(f"{unit.name}")

            print(f"\n--- Round {round_number} ---")
            print("Please enter the numbers of ALL your units in the order you want them to be attacked (separated by commas).")
            print("Or enter 'd' for default order.")
            for i, unit in enumerate(player2_units, start=1):
                print(f"{i}: {unit.name} (Health: {unit.health}, Attack: {unit.attack})")
            
            while True:
                try:
                    order_input = input("Enter ALL unit numbers in order (e.g. 1,2,3) or 'd' for default: ")
                    if order_input.lower() == 'd':
                        player2_attack_order = player2_units[:]
                        break
                    order = order_input.split(",")
                    if len(order) != len(player2_units):
                        print(f"Error: You must specify all {len(player2_units)} units.")
                        continue
                    if sorted([int(x) for x in order]) != list(range(1, len(player2_units) + 1)):
                        print("Error: You must use each number exactly once.")
                        continue
                    player2_attack_order = [player2_units[int(num)-1] for num in order]
                    break
                except (ValueError, IndexError):
                    print("Error: Invalid input. Use format like 1,2,3")

            print("Selected order:")
            for unit in player2_attack_order:
                print(f"{unit.name}")

            for turn in range(1, 4):  # Each round contains 3 turns
                print(f"\n--- Round {round_number} ---")
                print(f"\n--- Turn {turn} ---")
                player1.health, player2.health = battle_round(player1_units, player2_units, player1.health, player2.health, player1_attack_order, player2_attack_order)

                # Display health after each turn
                display_unit_health(player1_units, player2_units, player1.health, player2.health, player1_name="Player 1", player2_name="Player 2")

                result = check_victory(player1.health, player2.health, player1_name="Player 1", player2_name="Player 2")
                if result:
                    print(f"\n{result}")
                    return  # End the game if there's a victory
            player1.budget += 10
            player2.budget += 10
            player1_new_units, player1.budget = buy_units(player1.budget, player_number=1, player_units=player1_units)
            player2_new_units, player2.budget = buy_units(player2.budget, player_number=2, player_units=player2_units)
            player1_units.extend(player1_new_units)
            player2_units.extend(player2_new_units)

            round_number += 1

        # Display damage statistics
        plot_damage_stats(player1_units, player2_units, player1_name="Player 1", player2_name="Player 2")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    play_game_round(max_rounds=5)
