# utils.py

import random

def select_target(unit, opponent_units):
    living_targets = [enemy for enemy in opponent_units if enemy.is_alive()]
    if not living_targets:
        return None
    target = living_targets[0]
    return target

def apply_initial_faction_buffs(player_units):
    """
    Applies faction buffs at the start of the game.
    """
    faction_counts = {}
    for unit in player_units:
        faction = unit.faction
        faction_counts[faction] = faction_counts.get(faction, 0) + 1

    for faction, count in faction_counts.items():
        if count >= 3:
            # Apply the buff
            for unit in player_units:
                if unit.faction == faction:
                    unit.attack += 1 
                    unit.physical_defense += 1
                    unit.magical_defense += 1
            print(f"Buff applied: All units of {faction} gain +1 attack, +1 physical defense and +1 magical defense!")

def calculate_damage(attacker, defender):
    if attacker.attack_type == "physical":
        final_damage = max(attacker.attack - defender.physical_defense, 0)
    else:  # magical
        final_damage = max(attacker.attack - defender.magical_defense, 0)
    return final_damage
