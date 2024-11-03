# units/royalty.py

from utils import select_target
import random 
from .unit_base import Unit


class RoyalGuard(Unit):
    def __init__(self, faction):
        super().__init__('Royal Guard', 19, 8, 9, 5, 6, faction)

    def use_ability(self, allies, enemies):
        """
        Increases attack of all allies.
        """
        if self.ability_cooldown == 0:
            for ally in allies:
                if ally.is_alive():
                    ally.attack += 1
            self.ability_cooldown = 3
            print(f"{self.name} inspires allies, increasing their attack.")
        else:
            self.ability_cooldown = max(0, self.ability_cooldown - 1)

class QueenStrategist(Unit):
    def __init__(self, faction):
        super().__init__('Queen Strategist', 18, 6, 8, 5, 7, faction)
        self.turn_counter = 0

    def use_ability(self, allies, enemies):
        """
        Commands an ally to immediately attack.
        """
        if self.ability_cooldown == 0:
            # Exclude self and get living allies
            available_allies = [ally for ally in allies if ally.is_alive() and ally != self]
            if available_allies:
                ally = random.choice(available_allies)
                target = select_target(ally, enemies)
                if target:
                    print(f"{self.name} commands {ally.name} to immediately attack {target.name}!")
                    ally.attack_target(target)
                else:
                    print(f"{self.name} has no enemies for {ally.name} to attack.")
            else:
                print(f"{self.name} has no allies to command.")
            self.ability_cooldown = 3
        else:
            self.ability_cooldown = max(0, self.ability_cooldown - 1)

class KingWarlord(Unit):
    def __init__(self, faction):
        super().__init__('King Warlord', 20, 10, 11, 4, 8, faction)

    def use_ability(self, allies, enemies):
        """
        Increases defense of all allies.
        """
        if self.ability_cooldown == 0:
            for ally in allies:
                if ally.is_alive():
                    ally.defense += 2
            self.ability_cooldown = 3
            print(f"{self.name} increases the defense of all allies.")
        else:
            self.ability_cooldown = max(0, self.ability_cooldown - 1)