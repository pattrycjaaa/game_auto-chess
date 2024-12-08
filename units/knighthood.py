# units/knighthood.py

from utils import select_target
from .unit_base import Unit

class Knight(Unit):
    def __init__(self, faction):
        super().__init__('Knight', 18, 7, 8, 4, 5, 5, faction, "physical")  # health, attack, phys_def, mag_def, speed, mana
        self.ability_cooldown = 0

    def use_ability(self, allies, enemies):
        """
        Deals bonus physical damage equal to 50% of attack every third turn.
        """
        if self.ability_cooldown == 0:
            target = select_target(self, enemies)
            if target:
                bonus_damage = int(self.attack * 0.5)
                target.take_damage(bonus_damage, "physical")  # Specify damage type
                self.damage_dealt += bonus_damage
                self.ability_cooldown = 3
                print(f"{self.name} uses 'Power Strike' and deals {bonus_damage} physical bonus damage to {target.name}!")
        else:
            self.ability_cooldown -= 1

class Lancer(Unit):
    def __init__(self, faction):
        super().__init__('Lancer', 15, 8, 8, 2, 6, 6, faction, "physical")  # health, attack, phys_def, mag_def, speed
        self.charged = False
        self.ability_cooldown = 0

    def use_ability(self, allies, enemies):
        """
        First attack deals extra physical damage; can be used again after cooldown.
        """
        if not self.charged:
            target = select_target(self, enemies)
            if target:
                bonus_damage = 3
                target.take_damage(bonus_damage, "physical")  # Specify damage type
                self.damage_dealt += bonus_damage
                self.charged = True
                self.ability_cooldown = 2
                print(f"{self.name} charges and deals an extra {bonus_damage} physical damage to {target.name}!")
        elif self.ability_cooldown == 0:
            self.charged = False
        else:
            self.ability_cooldown -= 1

class ShieldBearer(Unit):
    def __init__(self, faction):
        super().__init__('Shield Bearer', 12, 6, 10, 3, 4, 5, faction, "physical")  # health, attack, phys_def, mag_def, speed
        self.ability_cooldown = 0

    def use_ability(self, allies, enemies):
        """
        Increases both physical and magical defense of all allies by 1.
        """
        if self.ability_cooldown == 0:
            for ally in allies:
                if ally.is_alive():
                    ally.physical_defense += 1
                    ally.magical_defense += 1  # Add magical defense boost
            self.ability_cooldown = 3
            print(f"{self.name} increases both physical and magical defense of all allies.")
        else:
            self.ability_cooldown -= 1
