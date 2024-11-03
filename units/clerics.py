# units/clerics.py

from utils import select_target
from .unit_base import Unit


class Healer(Unit):
    def __init__(self, faction):
        super().__init__('Healer', 13, 5, 6, 5, 4, faction)
        self.heal_cooldown = 0

    def use_ability(self, allies, enemies):
        """
        Heals the ally with the lowest health.
        """
        if self.heal_cooldown == 0:
            wounded_allies = [ally for ally in allies if ally.is_alive() and ally.health < ally.max_health]
            if wounded_allies:
                ally_to_heal = min(wounded_allies, key=lambda ally: ally.health)
                heal_amount = int(ally_to_heal.max_health * 0.2)
                ally_to_heal.health = min(ally_to_heal.max_health, ally_to_heal.health + heal_amount)
                self.heal_cooldown = 2  # Cooldown for 2 turns
                print(f"{self.name} heals {ally_to_heal.name} for {heal_amount} health.")
        else:
            self.heal_cooldown = max(0, self.heal_cooldown - 1)

class Monk(Unit):
    def __init__(self, faction):
        super().__init__('Monk', 17, 7, 7, 6, 5, faction)

    def use_ability(self, allies, enemies):
        """
        Reduces the target's attack temporarily.
        """
        if self.ability_cooldown == 0 and enemies:
            target = select_target(self, enemies)
            if target:
                target.attack = max(1, target.attack - 2)
                self.ability_cooldown = 3
                print(f"{self.name} reduces {target.name}'s attack by 2!")
        else:
            self.ability_cooldown = max(0, self.ability_cooldown - 1)

class Paladin(Unit):
    def __init__(self, faction):
        super().__init__('Paladin', 21, 9, 10, 4, 6, faction)

    def use_ability(self, allies, enemies):
        """
        Paladin heals itself slightly every turn.
        """
        if self.is_alive() and self.health < self.max_health:
            heal_amount = int(self.max_health * 0.1)
            self.health = min(self.max_health, self.health + heal_amount)
            print(f"{self.name} heals itself for {heal_amount} health.")