# units/archers.py

from utils import select_target
import random 
from .unit_base import Unit


class Archer(Unit):
    def __init__(self, faction):
        super().__init__('Archer', 17, 10, 5, 8, 4, faction)

    def use_ability(self, allies, enemies):
        """
        Deals extra damage if target has low defense.
        """
        target = select_target(self, enemies)
        if target and target.defense < 5:
            extra_damage = 5
            target.take_damage(extra_damage)
            self.damage_dealt += extra_damage
            print(f"{self.name} uses 'Precise Shot' on {target.name} and deals {extra_damage} extra damage!")

class Crossbowman(Unit):
    def __init__(self, faction):
        super().__init__('Crossbowman', 16, 12, 4, 7, 5, faction)

    def use_ability(self, allies, enemies):
        """
        Ignores 50% of the target's defense.
        """
        target = select_target(self, enemies)
        if target:
            ignored_defense = target.defense * 0.5
            actual_defense = target.defense - ignored_defense
            actual_damage = max(1, int(self.attack * (100 / (100 + actual_defense))))
            target.health -= actual_damage
            self.damage_dealt += actual_damage
            print(f"{self.name} pierces armor of {target.name}, ignoring 50% defense and deals {actual_damage} damage!")

class Longbowman(Unit):
    def __init__(self, faction):
        super().__init__('Longbowman', 18, 9, 3, 9, 5, faction)

    def use_ability(self, allies, enemies):
        """
        Attacks multiple enemies.
        """
        if self.ability_cooldown == 0:
            # Get the list of living enemies
            living_enemies = [unit for unit in enemies if unit.is_alive()]
            if living_enemies:
                # Determine k based on the number of living enemies
                k = min(2, len(living_enemies))
                targets = random.sample(living_enemies, k=k)
                for target in targets:
                    target.take_damage(self.attack)
                    self.damage_dealt += self.attack
                print(f"{self.name} uses 'Multi-Shot' and attacks multiple enemies!")
            else:
                print(f"{self.name} has no enemies to attack with 'Multi-Shot'.")
            self.ability_cooldown = 2
        else:
            self.ability_cooldown = max(0, self.ability_cooldown - 1)