# utils.py

import random

def select_target(unit, opponent_units):
    """
    Selects a target for the unit to attack based on strategy.
    """
    living_targets = [enemy for enemy in opponent_units if enemy.is_alive()]
    if not living_targets:
        return None
    # Select target with lowest health
    target = min(living_targets, key=lambda enemy: enemy.health)
    return target

def apply_faction_buffs(units):
    """
    Applies faction buffs to units if conditions are met.
    """
    faction_count = {}
    for unit in units:
        faction_count[unit.faction] = faction_count.get(unit.faction, 0) + 1

    # Apply buffs if there are 3 or more units from the same faction
    for faction, count in faction_count.items():
        if count >= 3:
            for unit in units:
                if unit.faction == faction:
                    unit.attack += 2
                    unit.defense += 2
            print(f"Buff applied: All units of {faction} gain +2 attack and +2 defense!")

def total_health(units):
    """
    Calculates the total health of living units.
    """
    return sum(unit.health for unit in units if unit.is_alive())
