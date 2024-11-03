# ai_player.py

import random
from shop import generate_unit_pool

class AIPlayer:
    """
    Represents an AI opponent that purchases and uses units.
    """
    def __init__(self, budget):
        self.budget = budget
        self.units = self.buy_units()

    def buy_units(self):
        """
        AI purchases units based on a simple strategy.
        """
        unit_pool = generate_unit_pool()
        purchased_units = []

        # Simple strategy: Buy units from the same faction
        factions = ['Knighthood', 'Royalty', 'Archers', 'Clerics']
        preferred_faction = random.choice(factions)

        while self.budget > 0 and unit_pool:
            affordable_units = [unit for unit in unit_pool if unit.cost <= self.budget]
            if not affordable_units:
                break
            # Prefer units from the preferred faction
            preferred_units = [unit for unit in affordable_units if unit.faction == preferred_faction]
            if preferred_units:
                unit = random.choice(preferred_units)
            else:
                unit = random.choice(affordable_units)
            purchased_units.append(unit)
            self.budget -= unit.cost
            unit_pool.remove(unit)
        print(f"AI purchased {len(purchased_units)} units.")
        return purchased_units
