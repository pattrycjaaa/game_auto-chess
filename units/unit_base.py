# units/unit_base.py

class Unit:
    """
    Base class for all units.
    """
    def __init__(self, name, health, attack, physical_defense, magical_defense, speed, cost, faction, damage_type="physical"):
        self.name = name  
        self.max_health = health
        self.health = health  
        self.attack = attack  
        self.physical_defense = physical_defense
        self.magical_defense = magical_defense
        self.speed = speed  
        self.cost = cost  
        self.faction = faction  
        self.damage_type = damage_type  # "physical" or "magical"
        self.damage_dealt = 0  
        self.ability_cooldown = 0  # Cooldown for abilities

    def take_damage(self, damage, damage_type="physical"):
        """
        Calculate and apply damage taken after defense mitigation.
        """
        defense = self.physical_defense if damage_type == "physical" else self.magical_defense
        actual_damage = max(1, int(damage * (100 / (100 + defense))))
        self.health -= actual_damage
        print(f"{self.name} takes {actual_damage} {damage_type} damage. Health: {self.health}")
        return actual_damage

    def attack_target(self, target):
        """
        Attack the target if the unit is alive.
        """
        if self.is_alive() and target.is_alive():
            # Pass damage type to take_damage
            damage = target.take_damage(self.attack, self.damage_type)
            self.damage_dealt += damage
            print(f"{self.name} attacks {target.name} for {damage} {self.damage_type} damage")

    def is_alive(self):
        """
        Check if the unit is still alive.
        """
        if self.health <= 0:
            return False
        return True
        
    def use_ability(self, allies, enemies):
        """
        Placeholder for units without special abilities.
        """
        pass
