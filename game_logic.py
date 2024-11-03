# game_logic.py

"""
game_logic.py

Contains the main game mechanics functions, including battle rounds, victory checks,
damage statistics plotting, and unit health display.
"""

from units import Unit
from utils import select_target, apply_faction_buffs
from matplotlib import pyplot as plt

def battle_round(player_units, opponent_units):
    """
    Conducts a battle round between player and opponent units.
    """
    # Apply faction buffs at the start
    apply_faction_buffs(player_units)
    apply_faction_buffs(opponent_units)

    # Sort units by speed
    all_units = sorted(player_units + opponent_units, key=lambda unit: unit.speed, reverse=True)
    for unit in all_units:
        if unit.is_alive():
            if unit in player_units:
                allies = player_units
                enemies = opponent_units
            else:
                allies = opponent_units
                enemies = player_units

            # Unit attacks
            target = select_target(unit, enemies)
            if target:
                unit.attack_target(target)
            else:
                print(f"{unit.name} has no targets to attack.")
            # Unit uses ability
            unit.use_ability(allies, enemies)

def check_victory(player_units, opponent_units):
    """
    Checks if there is a victory condition met.
    """
    player_alive = any(unit.is_alive() for unit in player_units)
    opponent_alive = any(unit.is_alive() for unit in opponent_units)
    if not player_alive and not opponent_alive:
        return "Draw"
    elif player_alive and not opponent_alive:
        return "Player wins"
    elif opponent_alive and not player_alive:
        return "Opponent wins"
    return None

def plot_damage_stats(player_units, opponent_units):
    """
    Visualizes damage statistics for units.
    """
    units = player_units + opponent_units
    names = [unit.name + (" (Player)" if unit in player_units else " (Opponent)") for unit in units]
    damage = [unit.damage_dealt for unit in units]
    health = [max(0, unit.health) for unit in units]  # Ensure health doesn't go below 0

    # Plot damage dealt and remaining health
    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    index = range(len(units))

    plt.bar(index, damage, bar_width, color='red', label='Damage Dealt')
    plt.bar(index, health, bar_width, bottom=damage, color='green', label='Remaining Health')

    plt.xlabel('Units')
    plt.ylabel('Values')
    plt.title('Damage Dealt and Remaining Health by Units in Battle')
    plt.xticks(index, names, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Additional unit information
    print("\n--- Unit Statistics ---")
    for unit in units:
        owner = "Player" if unit in player_units else "Opponent"
        status = f"Health = {unit.health}/{unit.max_health}" if unit.is_alive() else "Dead"
        print(f"{unit.name} ({owner}): {status}, Damage Dealt = {unit.damage_dealt}")

def display_unit_health(player_units, opponent_units):
    """
    Displays the current health of all units.
    """
    print("\n--- Current Unit Health ---")
    print("Player Units:")
    for unit in player_units:
        status = f"{unit.health}/{unit.max_health}" if unit.is_alive() else "Dead"
        print(f"  {unit.name}: {status}")
    print("Opponent Units:")
    for unit in opponent_units:
        status = f"{unit.health}/{unit.max_health}" if unit.is_alive() else "Dead"
        print(f"  {unit.name}: {status}")
