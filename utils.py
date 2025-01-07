# utils.py

import random

def select_target(unit, opponent_units):
    """
    Example "manual" targeting function. 
    For a real player, you might ask input from the console or GUI.
    Here, we just pick the first living opponent.
    """
    living_targets = [enemy for enemy in opponent_units if enemy.is_alive()]
    if not living_targets:
        return None
    return living_targets[0]

def update_buffs_and_debuffs(units):
    """
    Expires or removes buffs/debuffs after each turn.
    (Przeniesione z game_logic.py do utils.py)
    """
    for unit in units:
        # --- Attack buff (np. RoyalGuard) ---
        if hasattr(unit, 'attack_buff_duration'):
            if unit.attack_buff_duration > 0:
                unit.attack_buff_duration -= 1
                if unit.attack_buff_duration == 0:
                    unit.attack -= 1
                    print(f"{unit.name}'s attack buff has expired.")
                    del unit.attack_buff_duration
            else:
                del unit.attack_buff_duration

        # --- Physical defense buff (np. KingWarlord, ShieldBearer) ---
        if hasattr(unit, 'physical_defense_buff_duration'):
            if unit.physical_defense_buff_duration > 0:
                unit.physical_defense_buff_duration -= 1
                if unit.physical_defense_buff_duration == 0:
                    unit.physical_defense -= 1
                    print(f"{unit.name}'s physical defense buff has expired.")
                    del unit.physical_defense_buff_duration
            else:
                del unit.physical_defense_buff_duration

        # --- Magical defense buff (np. KingWarlord, ShieldBearer) ---
        if hasattr(unit, 'magical_defense_buff_duration'):
            if unit.magical_defense_buff_duration > 0:
                unit.magical_defense_buff_duration -= 1
                if unit.magical_defense_buff_duration == 0:
                    unit.magical_defense -= 1
                    print(f"{unit.name}'s magical defense buff has expired.")
                    del unit.magical_defense_buff_duration
            else:
                del unit.magical_defense_buff_duration

        # --- Attack debuff (np. Monk) ---
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
                if hasattr(unit, 'attack_debuff_amount'):
                    del unit.attack_debuff_amount

def apply_initial_faction_buffs(player_units):
    """
    Applies faction buffs at the start of the game 
    if a player has at least 3 units from the same faction.
    """
    faction_counts = {}
    for unit in player_units:
        faction = unit.faction
        faction_counts[faction] = faction_counts.get(faction, 0) + 1

    for faction, count in faction_counts.items():
        if count >= 3:
            for unit in player_units:
                if unit.faction == faction:
                    unit.attack += 1
                    unit.physical_defense += 1
                    unit.magical_defense += 1
            print(f"Buff applied: All units of {faction} gain +1 attack, +1 physical defense, +1 magical defense!")

def ai_select_target(unit, opponent_units):
    """
    AI selects a target based on a simple decision tree:
    1. Prioritize units with the highest attack.
    2. If multiple have same attack, pick the one with the lowest health.
    """
    living_targets = [enemy for enemy in opponent_units if enemy.is_alive()]
    if not living_targets:
        return None

    living_targets.sort(key=lambda u: (-u.attack, u.health))
    target = living_targets[0]
    print(f"{unit.name} (AI) selects {target.name} as the target.")
    return target
