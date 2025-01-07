# units/archers.py

from utils import select_target
import random
from .unit_base import Unit

class Archer(Unit):
    def __init__(self, faction):
        super().__init__('Archer', 17, 6, 5, 3, 8, 4, faction, "physical")

    def use_ability(self, allies, enemies):
        """
        Deals extra damage if target has low physical defense.
        """
        target = select_target(self, enemies)
        if target and target.physical_defense < 6:
            extra_damage = 3
            target.take_damage(extra_damage, "physical")
            self.damage_dealt += extra_damage
            print(f"{self.name} uses 'Precise Shot' on {target.name} and deals {extra_damage} physical damage!")

class Crossbowman(Unit):
    def __init__(self, faction):
        super().__init__('Crossbowman', 16, 9, 4, 3, 7, 5, faction, "physical")

    def use_ability(self, allies, enemies):
        """
        Ignores 30% of the target's physical defense.
        """
        target = select_target(self, enemies)
        if target:
            ignored_defense = target.physical_defense * 0.3
            actual_defense = max(0, target.physical_defense - ignored_defense)
            damage = max(1, self.attack - int(actual_defense))
            target.take_damage(damage, "physical")
            self.damage_dealt += damage
            print(f"{self.name} pierces armor of {target.name}, ignoring 30% physical defense and deals {damage} damage!")

class Longbowman(Unit):
    def __init__(self, faction):
        super().__init__('Longbowman', 18, 7, 3, 3, 9, 5, faction, "physical")
        self.ability_cooldown = 0

    def use_ability(self, allies, enemies):
        """
        Attacks multiple enemies with reduced physical damage.
        Every time ability is used, it goes on a 3-turn cooldown.
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
                        damage = int(self.attack * 0.5)
                    target.take_damage(damage, "physical")
                    self.damage_dealt += damage
                    print(f"{self.name} attacks {target.name} and deals {damage} physical damage.")
            else:
                print(f"{self.name} has no enemies to attack with 'Multi-Shot'.")
            self.ability_cooldown = 3
        else:
            self.ability_cooldown -= 1
