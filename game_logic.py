# game_logic.py

from units import Unit
from utils import select_target, apply_initial_faction_buffs
from matplotlib import pyplot as plt

def battle_round(player1_units, player2_units, player1_health, player2_health, player1_order, player2_order):
    # Apply faction buffs at the start of each round
    apply_initial_faction_buffs(player1_units)
    apply_initial_faction_buffs(player2_units)

    # Get all units
    all_units = player1_units + player2_units
    # Sort units by speed in descending order
    units_in_order = sorted(all_units, key=lambda unit: unit.speed, reverse=True)

    for unit in units_in_order:
        if unit.is_alive():
            if unit in player1_units:
                allies = player1_units
                enemies = player2_order
            else:
                allies = player2_units
                enemies = player1_order

            # Unit uses ability
            unit.use_ability(allies, enemies)
            # Unit attacks
            target = select_target(unit, enemies)
            if target:
                unit.attack_target(target)
            else:
                print(f"{unit.name} has no target and attacks the player directly.")
                if unit in player1_units:
                    player2_health -= unit.attack
                else:
                    player1_health -= unit.attack

    update_buffs_and_debuffs(player1_units + player2_units)
    return player1_health, player2_health

def check_victory(player1_health, player2_health, player1_name="Player 1", player2_name="Player 2"):
    """
    Checks if there is a victory condition met.
    """
    if player1_health >= 0 and player2_health <= 0:
        return f"{player1_name} wins"
    elif player2_health >= 0 and player1_health <= 0:
        return f"{player2_name} wins"
    elif player1_health <= 0 and player2_health <= 0:
        return "It's a draw"
    return None

def plot_damage_stats(player1_units, player2_units, player1_name="Player 1", player2_name="Player 2"):
    """
    Visualizes damage statistics for units.
    """
    units = player1_units + player2_units
    names = [unit.name + f" ({player1_name})" if unit in player1_units else unit.name + f" ({player2_name})" for unit in units]
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
        owner = player1_name if unit in player1_units else player2_name
        status = f"Health = {unit.health}/{unit.max_health}" if unit.is_alive() else "Dead"
        print(f"{unit.name} ({owner}): {status}, Damage Dealt = {unit.damage_dealt}")

def display_unit_health(player1_units, player2_units, player1_health, player2_health, player1_name="Player 1", player2_name="Player 2"):
    """
    Displays the current health of all units.
    """
    print ("\n--- Current Player Health ---")
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

def update_buffs_and_debuffs(units):
    for unit in units:
        # Handle attack buffs
        if hasattr(unit, 'attack_buff_duration'):
            if unit.attack_buff_duration > 0:
                unit.attack_buff_duration -= 1
                if unit.attack_buff_duration == 0:
                    unit.attack -= 1
                    print(f"{unit.name}'s attack buff has expired.")
                    del unit.attack_buff_duration
            else:
                del unit.attack_buff_duration

        # Handle physical defense buffs
        if hasattr(unit, 'physical_defense_buff_duration'):
            if unit.physical_defense_buff_duration > 0:
                unit.physical_defense_buff_duration -= 1
                if unit.physical_defense_buff_duration == 0:
                    unit.physical_defense -= 1
                    print(f"{unit.name}'s physical defense buff has expired.")
                    del unit.physical_defense_buff_duration
            else:
                del unit.physical_defense_buff_duration

        # Handle magical defense buffs
        if hasattr(unit, 'magical_defense_buff_duration'):
            if unit.magical_defense_buff_duration > 0:
                unit.magical_defense_buff_duration -= 1
                if unit.magical_defense_buff_duration == 0:
                    unit.magical_defense -= 1
                    print(f"{unit.name}'s magical defense buff has expired.")
                    del unit.magical_defense_buff_duration
            else:
                del unit.magical_defense_buff_duration

        # Handle attack debuffs
        if hasattr(unit, 'attack_debuff_duration'):
            if unit.attack_debuff_duration > 0:
                unit.attack_debuff_duration -= 1
                if unit.attack_debuff_duration == 0:
                    unit.attack += unit.attack_debuff_amount
                    print(f"{unit.name}'s attack debuff has worn off.")
                    del unit.attack_debuff_duration
                    del unit.attack_debuff_amount
            else:
                del unit.attack_debuff_duration
                del unit.attack_debuff_amount