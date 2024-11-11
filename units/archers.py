# units/archers.py

from utils import select_target
import random
from .unit_base import Unit

class Archer(Unit):
    def __init__(self, faction):
        super().__init__('Archer', 17, 6, 5, 8, 4, faction)

    def use_ability(self, allies, enemies):
        """
        Deals extra damage if target has low defense.
        """
        target = select_target(self, enemies)
        if target and target.defense < 6:  # Adjusted defense threshold
            extra_damage = 3  # Reduced extra damage
            target.take_damage(extra_damage)
            self.damage_dealt += extra_damage
            print(f"{self.name} uses 'Precise Shot' on {target.name} and deals {extra_damage} extra damage!")

class Crossbowman(Unit):
    def __init__(self, faction):
        super().__init__('Crossbowman', 16, 9, 4, 7, 5, faction)  # Reduced attack

    def use_ability(self, allies, enemies):
        """
        Ignores 30% of the target's defense.
        """
        target = select_target(self, enemies)
        if target:
            ignored_defense = target.defense * 0.3  # Adjusted to 30%
            actual_defense = max(0, target.defense - ignored_defense)
            damage = max(1, self.attack - actual_defense)
            target.take_damage(damage)
            self.damage_dealt += damage
            print(f"{self.name} pierces armor of {target.name}, ignoring 30% defense and deals {damage} damage!")

class Longbowman(Unit):
    def __init__(self, faction):
        super().__init__('Longbowman', 18, 7, 3, 9, 5, faction)
        self.ability_cooldown = 0

    def use_ability(self, allies, enemies):
        """
        Attacks multiple enemies with reduced damage.
        """
        if self.ability_cooldown == 0:
            living_enemies = [unit for unit in enemies if unit.is_alive()]
            if living_enemies:
                targets = random.sample(living_enemies, k=min(2, len(living_enemies)))
                print(f"{self.name} uses 'Multi-Shot' and attacks multiple enemies!")
                for i, target in enumerate(targets):
                    if i == 0:
                        damage = self.attack
                    else:
                        damage = int(self.attack * 0.5)  # Additional targets take 50% damage
                    target.take_damage(damage)
                    self.damage_dealt += damage
                    print(f"{self.name} attacks {target.name} and deals {damage} damage.")
            else:
                print(f"{self.name} has no enemies to attack with 'Multi-Shot'.")
            self.ability_cooldown = 3  # Increased cooldown
        else:
            self.ability_cooldown -= 1
