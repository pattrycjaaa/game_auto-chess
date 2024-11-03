# units/unit_base.py

import random 

class Unit:
    """
    Base class for all units.
    """
    def __init__(self, name, health, attack, defense, speed, cost, faction):
        self.name = name  
        self.max_health = health
        self.health = health  
        self.attack = attack  
        self.defense = defense  
        self.speed = speed  
        self.cost = cost  
        self.faction = faction  
        self.damage_dealt = 0  
        self.ability_cooldown = 0  # Cooldown for abilities

    def take_damage(self, damage):
        """
        Calculate and apply damage taken after defense mitigation.
        """
        # Improved damage calculation using a more nuanced formula
        actual_damage = max(1, int(damage * (100 / (100 + self.defense))))
        self.health -= actual_damage
        print(f"{self.name} takes {actual_damage} damage. Health: {self.health}")

    def attack_target(self, target):
        """
        Attack the target if the unit is alive.
        """
        if self.is_alive():
            target.take_damage(self.attack)
            self.damage_dealt += self.attack
            print(f"{self.name} attacks {target.name} and deals {self.attack} damage.")

    def is_alive(self):
        """
        Check if the unit is still alive.
        """
        return self.health > 0

    def use_ability(self, allies, enemies):
        """
        Placeholder for units without special abilities.
        """
        pass
