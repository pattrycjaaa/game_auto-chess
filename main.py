# main.py

from player import Player
from ai_player import AIPlayer
from shop import Shop, buy_units
from game_logic import battle_round, check_victory, plot_damage_stats, display_unit_health
import traceback

def play_game_round(max_rounds=5):
    try:
        # Tworzymy gracza i AI
        player1 = Player(name="Player 1")
        player2 = AIPlayer(budget=20)  # np. AI z budżetem 20
        shop = Shop()

        # Player 1 kupuje jednostki
        print("Player 1, build your army!")
        player1_units, player1.budget = buy_units(player1.budget, 1, None, shop)

        # AI kupuje jednostki
        print("\nAI is building its army!")
        player2.buy_units()  # Metoda w klasie AIPlayer
        player2_units = player2.units

        # Rozgrywka (max_rounds rund)
        round_number = 1
        while round_number <= max_rounds:
            print(f"\n--- Round {round_number} ---")

            # Sprawdzamy, czy Player 1 w ogóle ma żywe jednostki
            alive_player1_units = [u for u in player1_units if u.is_alive()]
            if not alive_player1_units:
                print("Player 1 has no alive units left.")
                break

            # 1. Player 1 wybiera kolejność ataku
            print("Player 1, enter the attack order for your alive units.")
            print("Or enter 'd' for default order.")
            for i, unit in enumerate(alive_player1_units, start=1):
                print(f"{i}: {unit.name} (Health: {unit.health}, Attack: {unit.attack})")

            while True:
                order_input = input("Enter ALL unit numbers in order (e.g. 1,2,3) or 'd' for default: ")
                if order_input.lower() == 'd':
                    player1_attack_order = alive_player1_units[:]
                    break
                else:
                    try:
                        order = order_input.split(",")
                        if len(order) != len(alive_player1_units):
                            print(f"Error: You must specify all {len(alive_player1_units)} units.")
                            continue
                        # Sprawdzamy, czy numery są w zakresie
                        if sorted([int(x) for x in order]) != list(range(1, len(alive_player1_units)+1)):
                            print("Error: You must use each number exactly once.")
                            continue
                        player1_attack_order = [alive_player1_units[int(num)-1] for num in order]
                        break
                    except (ValueError, IndexError):
                        print("Error: Invalid input. Use format like 1,2,3")

            # 2. AI ustala kolejność ataku (np. według speed)
            player2_attack_order = player2.choose_attack_order()
            # (domyślnie w choose_attack_order() -> sortowanie malejąco po speed)

            # 3. Każda runda ma np. 3 tury
            for turn in range(1, 4):
                print(f"\n--- Turn {turn} ---")
                # Tutaj wywołujemy battle_round ze specjalną logiką interleaving
                player1.health, player2.health = battle_round(
                    player1_units, player2_units,
                    player1.health, player2.health,
                    player1_attack_order,
                    player2_attack_order
                )

                # Wyświetlamy stan po turze
                display_unit_health(
                    player1_units, player2_units,
                    player1.health, player2.health,
                    player1_name="Player 1", player2_name="AI"
                )

                # Sprawdzamy warunek zwycięstwa
                result = check_victory(
                    player1.health, player2.health,
                    player1_name="Player 1", player2_name="AI"
                )
                if result:
                    print(f"\n{result}")
                    return  # kończy grę

            # Możemy przyznać dodatkowy budżet po rundzie
            player1.budget += 10
            player2.budget += 10

            # Pozwalamy dokupić jednostki (opcjonalnie) po rundzie
            player1_new_units, player1.budget = buy_units(player1.budget, 1, None, shop)
            player1_units.extend(player1_new_units)

            player2.buy_units()  # AI dokupuje
            player2_units = player2.units

            round_number += 1

        # Koniec wszystkich rund – statystyki
        plot_damage_stats(player1_units, player2_units, player1_name="Player 1", player2_name="AI")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    play_game_round(max_rounds=5)
