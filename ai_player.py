# ai_player.py

from shop import Shop

class AIPlayer:
    """
    Represents an AI opponent that uses a decision tree for choosing units and strategies.
    """
    def __init__(self, budget):
        self.name = "AI Player"
        self.health = 100       # <-- DODANE POLE HEALTH
        self.budget = budget
        self.units = []
        self.preferred_faction = None
        self.shop = Shop()

    def select_preferred_faction(self):
        """
        Decide on a preferred faction based on a new random unit pool.
        (AI tries to focus on a faction that is abundant in the pool)
        """
        unit_pool = self.shop.generate_unit_pool()
        faction_counts = {}
        for unit in unit_pool:
            faction_counts[unit.faction] = faction_counts.get(unit.faction, 0) + 1

        self.preferred_faction = max(faction_counts, key=faction_counts.get)
        print(f"AI prefers faction: {self.preferred_faction}")

    def buy_units(self):
        """
        AI purchases units based on a decision tree:
         - If no preferred faction, pick one with the largest presence in a random pool
         - Buy units of that faction first (or fallback to best stats)
        """
        unit_pool = self.shop.generate_unit_pool()

        if not self.preferred_faction:
            self.select_preferred_faction()

        while self.budget > 0 and unit_pool:
            affordable_units = [unit for unit in unit_pool if unit.cost <= self.budget]

            preferred_units = [u for u in affordable_units if u.faction == self.preferred_faction]

            if preferred_units:
                unit = max(preferred_units, key=lambda u: (u.attack, u.speed))
            elif affordable_units:
                unit = max(affordable_units, key=lambda u: (u.attack, u.speed))
            else:
                break

            self.units.append(unit)
            self.budget -= unit.cost
            unit_pool.remove(unit)
            print(f"AI purchased {unit.name} (Faction: {unit.faction}, Attack: {unit.attack}, Speed: {unit.speed}).")

        print(f"AI has {len(self.units)} units after purchasing.")

    def choose_attack_order(self):
        """
        Automatically determines the attack order for the AI's units.
        Here: simple approach -> sort descending by speed
        """
        self.units = sorted([unit for unit in self.units if unit.is_alive()], key=lambda u: -u.speed)
        print("AI attack order determined:")
        for unit in self.units:
            print(f"  {unit.name} (Speed: {unit.speed})")
        return self.units
