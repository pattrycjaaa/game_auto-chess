# units/royalty.py

from utils import select_target
import random
from .unit_base import Unit

class RoyalGuard(Unit):
    def __init__(self, faction):
        super().__init__('Royal Guard', 19, 8, 9, 5, 5, 6, faction, "physical")
        self.ability_cooldown = 0

    def use_ability(self, allies, enemies):
        """
        Temporarily increases attack of all allies.
        """
        if self.ability_cooldown == 0:
            for ally in allies:
                if ally.is_alive():
                    ally.attack += 1
                    ally.attack_buff_duration = 2  # Effect lasts for 2 turns
            self.ability_cooldown = 3
            print(f"{self.name} inspires allies, increasing their attack for 2 turns.")
        else:
            self.ability_cooldown -= 1

class QueenStrategist(Unit):
    def __init__(self, faction):
        super().__init__('Queen Strategist', 20, 6, 7, 7, 7, 7, faction, "magical")
        self.ability_cooldown = 0

    def use_ability(self, allies, enemies):
        """
        Commands an ally with lower speed to immediately attack.
        """
        if self.ability_cooldown == 0:
            available_allies = [ally for ally in allies if ally.is_alive() and ally.speed < self.speed and ally != self]
            if available_allies:
                ally = random.choice(available_allies)
                target = select_target(ally, enemies)
                if target:
                    print(f"{self.name} commands {ally.name} to immediately attack {target.name}!")
                    ally.attack_target(target)
                else:
                    print(f"{self.name} has no enemies for {ally.name} to attack.")
            else:
                print(f"{self.name} has no suitable allies to command.")
            self.ability_cooldown = 4  # Increased cooldown
        else:
            self.ability_cooldown -= 1

class KingWarlord(Unit):
    def __init__(self, faction):
        super().__init__('King Warlord', 20, 8, 11, 4, 4, 8, faction, "physical")  # Reduced attack from 10 to 8
        self.ability_cooldown = 0

    def use_ability(self, allies, enemies):
        """
        Increases physical and magical defense of all allies by 1.
        """
        if self.ability_cooldown == 0:
            for ally in allies:
                if ally.is_alive():
                    ally.physical_defense += 1  
                    ally.magical_defense += 1  
                    ally.defense_buff_duration = 2  
            self.ability_cooldown = 3 
            print(f"{self.name} increases the physical and magical defense of all allies.")
        else:
            self.ability_cooldown -= 1
