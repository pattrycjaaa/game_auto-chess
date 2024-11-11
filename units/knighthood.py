# units/knighthood.py

from utils import select_target
from .unit_base import Unit

class Knight(Unit):
    def __init__(self, faction):
        super().__init__('Knight', 18, 7, 8, 5, 5, faction)  # Reduced defense
        self.ability_cooldown = 0

    def use_ability(self, allies, enemies):
        """
        Deals bonus damage equal to 50% of attack every third turn.
        """
        if self.ability_cooldown == 0:
            target = select_target(self, enemies)
            if target:
                bonus_damage = int(self.attack * 0.5)  # Adjusted bonus damage
                target.take_damage(bonus_damage)
                self.damage_dealt += bonus_damage
                self.ability_cooldown = 3
                print(f"{self.name} uses 'Power Strike' and deals {bonus_damage} bonus damage to {target.name}!")
        else:
            self.ability_cooldown -= 1

class Lancer(Unit):
    def __init__(self, faction):
        super().__init__('Lancer', 15, 8, 8, 6, 6, faction)
        self.charged = False
        self.ability_cooldown = 0

    def use_ability(self, allies, enemies):
        """
        First attack deals extra damage; can be used again after cooldown.
        """
        if not self.charged:
            target = select_target(self, enemies)
            if target:
                bonus_damage = 3  # Reduced bonus damage
                target.take_damage(bonus_damage)
                self.damage_dealt += bonus_damage
                self.charged = True
                self.ability_cooldown = 2  # Added cooldown
                print(f"{self.name} charges and deals an extra {bonus_damage} damage to {target.name}!")
        elif self.ability_cooldown == 0:
            self.charged = False
        else:
            self.ability_cooldown -= 1

class ShieldBearer(Unit):
    def __init__(self, faction):
        super().__init__('Shield Bearer', 12, 6, 10, 4, 5, faction)  # Reduced defense
        self.ability_cooldown = 0

    def use_ability(self, allies, enemies):
        """
        Increases defense of all allies by 1.
        """
        if self.ability_cooldown == 0:
            for ally in allies:
                if ally.is_alive():
                    ally.defense += 1  # Reduced defense boost
            self.ability_cooldown = 3
            print(f"{self.name} increases the defense of all allies.")
        else:
            self.ability_cooldown -= 1
