# units/knighthood.py

from utils import select_target  
from .unit_base import Unit


class Knight(Unit):
    def __init__(self, faction):
        super().__init__('Knight', 20, 8, 10, 5, 5, faction)

    def use_ability(self, allies, enemies):
        """
        Knight's ability to deal double damage every third turn.
        """
        if self.ability_cooldown == 0 and enemies:
            target = select_target(self, enemies)
            if target:
                bonus_damage = self.attack
                target.take_damage(bonus_damage)
                self.damage_dealt += bonus_damage
                self.ability_cooldown = 3  # Cooldown for 3 turns
                print(f"{self.name} uses 'Power Strike' and deals {bonus_damage} bonus damage to {target.name}!")
        else:
            self.ability_cooldown = max(0, self.ability_cooldown - 1)

class Lancer(Unit):
    def __init__(self, faction):
        super().__init__('Lancer', 15, 10, 8, 6, 6, faction)
        self.charged = False

    def use_ability(self, allies, enemies):
        """
        Lancer's first attack deals extra damage.
        """
        if not self.charged and enemies:
            target = select_target(self, enemies)
            if target:
                bonus_damage = 5
                target.take_damage(bonus_damage)
                self.damage_dealt += bonus_damage
                self.charged = True
                print(f"{self.name} charges and deals an extra {bonus_damage} damage to {target.name}!")

class ShieldBearer(Unit):
    def __init__(self, faction):
        super().__init__('Shield Bearer', 12, 6, 12, 4, 5, faction)

    def use_ability(self, allies, enemies):
        """
        Increases defense of all allies by 2.
        """
        if self.ability_cooldown == 0:
            for ally in allies:
                if ally.is_alive():
                    ally.defense += 2
            self.ability_cooldown = 3  # Cooldown for 3 turns
            print(f"{self.name} increases the defense of all allies.")
        else:
            self.ability_cooldown = max(0, self.ability_cooldown - 1)