# game_logic.py

from utils import select_target, update_buffs_and_debuffs

def battle_round(
    player1_units,
    player2_units,
    player1_health,
    player2_health,
    player1_order,
    player2_order
):
    """
    Interleaved battle: p1_order[0] atakuje, potem p2_order[0], potem p1_order[1] itd.
    """

    # maks. długość większej z dwóch list
    max_len = max(len(player1_order), len(player2_order))

    for i in range(max_len):
        # Atak gracza 1 (jeśli i-ty unit istnieje i żyje)
        if i < len(player1_order):
            unit = player1_order[i]
            if unit.is_alive():
                # Znajdź żywego wroga
                enemies = [u for u in player2_units if u.is_alive()]
                if enemies:
                    # Wybierz cel (np. prosty: pierwszy żywy, lub inny system)
                    target = select_target(unit, enemies)
                    # Użyj zdolności, jeśli jest
                    unit.use_ability(player1_units, player2_units)
                    # Atak
                    if target and target.is_alive():
                        unit.attack_target(target)
                    else:
                        # Bezpośrednio w health przeciwnika (jeśli nie ma jednostek)
                        player2_health -= unit.attack

        # Atak gracza 2 (AI) – analogicznie
        if i < len(player2_order):
            unit = player2_order[i]
            if unit.is_alive():
                enemies = [u for u in player1_units if u.is_alive()]
                if enemies:
                    target = select_target(unit, enemies)
                    unit.use_ability(player2_units, player1_units)
                    if target and target.is_alive():
                        unit.attack_target(target)
                    else:
                        player1_health -= unit.attack

    # Na koniec TURY aktualizujemy buffy i debuffy
    update_buffs_and_debuffs(player1_units + player2_units)

    return player1_health, player2_health


def check_victory(player1_health, player2_health, player1_name="Player 1", player2_name="Player 2"):
    """
    Checks if there is a victory condition met.
    """
    if player1_health > 0 and player2_health <= 0:
        return f"{player1_name} wins"
    elif player2_health > 0 and player1_health <= 0:
        return f"{player2_name} wins"
    elif player1_health <= 0 and player2_health <= 0:
        return "It's a draw"
    return None


def plot_damage_stats(player1_units, player2_units,
                      player1_name="Player 1", player2_name="Player 2"):
    """
    Visualizes damage statistics for units (optional feature).
    """
    import matplotlib.pyplot as plt
    import numpy as np

    units = player1_units + player2_units
    names = [
        f"{unit.name} ({player1_name})" if unit in player1_units 
        else f"{unit.name} ({player2_name})"
        for unit in units
    ]
    damage = [unit.damage_dealt for unit in units]
    health = [max(0, unit.health) for unit in units]  # Ensure health doesn't go below 0

    # Plot damage dealt and remaining health
    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    index = np.arange(len(units))

    plt.bar(index, damage, bar_width, color='red', label='Damage Dealt')
    plt.bar(index, health, bar_width, bottom=damage, color='green', label='Remaining Health')

    plt.xlabel('Units')
    plt.ylabel('Values')
    plt.title('Damage Dealt and Remaining Health by Units in Battle')
    plt.xticks(index, names, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Additional unit information in console
    print("\n--- Unit Statistics ---")
    for unit in units:
        owner = player1_name if unit in player1_units else player2_name
        status = f"Health = {unit.health}/{unit.max_health}" if unit.is_alive() else "Dead"
        print(f"{unit.name} ({owner}): {status}, Damage Dealt = {unit.damage_dealt}")


def display_unit_health(player1_units, player2_units,
                        player1_health, player2_health,
                        player1_name="Player 1",
                        player2_name="Player 2"):
    """
    Displays the current health of all units.
    """
    print("\n--- Current Player Health ---")
    print(f"{player1_name}: {player1_health}")
    print(f"{player2_name}: {player2_health}")
    print("\n--- Current Unit Health ---")
    print(f"{player1_name} Units:")
    for unit in player1_units:
        status = f"{unit.health}/{unit.max_health}" if unit.is_alive() else "Dead"
        print(f"  {unit.name}: {status}")

    print(f"{player2_name} Units:")
    for unit in player2_units:
        status = f"{unit.health}/{unit.max_health}" if unit.is_alive() else "Dead"
        print(f"  {unit.name}: {status}")
