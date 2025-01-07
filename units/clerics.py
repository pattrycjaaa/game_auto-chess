# units/clerics.py

from utils import select_target
from .unit_base import Unit

class Healer(Unit):
    def __init__(self, faction):
        super().__init__('Healer', 13, 5, 4, 6, 4, 6, faction, "magical")
        self.heal_cooldown = 0

    def use_ability(self, allies, enemies):
        """
        Heals the ally with the lowest health (15% of max_health).
        Ability has a 3-turn cooldown.
        """
        if self.heal_cooldown == 0:
            wounded_allies = [ally for ally in allies if ally.is_alive() and ally.health < ally.max_health]
            if wounded_allies:
                ally_to_heal = min(wounded_allies, key=lambda ally: ally.health)
                heal_amount = int(ally_to_heal.max_health * 0.15)
                ally_to_heal.health = min(ally_to_heal.max_health, ally_to_heal.health + heal_amount)
                self.heal_cooldown = 3
                print(f"{self.name} heals {ally_to_heal.name} for {heal_amount} health.")
        else:
            self.heal_cooldown -= 1

class Monk(Unit):
    def __init__(self, faction):
        super().__init__('Monk', 12, 6, 3, 7, 6, 5, faction, "physical")
        self.ability_cooldown = 0

    def use_ability(self, allies, enemies):
        """
        Debuffs target's attack by 1 for 2 turns.
        Cooldown: 4 turns.
        """
        if self.ability_cooldown == 0:
            target = select_target(self, enemies)
            if target:
                # Sprawdzamy, czy nie ma już debuffa
                if not hasattr(target, 'attack_debuff_duration'):
                    target.attack_debuff_amount = 1
                    target.attack_debuff_duration = 2
                    target.attack -= target.attack_debuff_amount
                    self.ability_cooldown = 4
                    print(f"{self.name} reduces {target.name}'s attack by 1 for 2 turns!")
            else:
                print(f"{self.name} has no enemies to debuff.")
        else:
            self.ability_cooldown -= 1

class Paladin(Unit):
    def __init__(self, faction):
        super().__init__('Paladin', 21, 9, 5, 9, 4, 6, faction, "physical")

    def use_ability(self, allies, enemies):
        """
        Paladin heals itself slightly every turn (5% max_health).
        No specific cooldown, triggers each turn if alive.
        """
        if self.is_alive() and self.health < self.max_health:
            heal_amount = max(1, int(self.max_health * 0.05))
            self.health = min(self.max_health, self.health + heal_amount)
            print(f"{self.name} heals itself for {heal_amount} health.")
