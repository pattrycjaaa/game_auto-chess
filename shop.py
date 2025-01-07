# shop.py

import random
from units.archers import Archer, Crossbowman, Longbowman
from units.clerics import Healer, Monk, Paladin
from units.knighthood import Knight, Lancer, ShieldBearer
from units.royalty import RoyalGuard, QueenStrategist, KingWarlord

UNIT_FACTIONS = {
    Archer: 'Archers',
    Crossbowman: 'Archers',
    Longbowman: 'Archers',
    Healer: 'Clerics',
    Monk: 'Clerics',
    Paladin: 'Clerics',
    Knight: 'Knighthood',
    Lancer: 'Knighthood',
    ShieldBearer: 'Knighthood',
    RoyalGuard: 'Royalty',
    QueenStrategist: 'Royalty',
    KingWarlord: 'Royalty'
}

class Shop:
    def __init__(self):
        self.player_shops = {}  # Sklepy dla każdego gracza
        self.possible_units = [
            Knight, Lancer, ShieldBearer,
            Archer, Crossbowman, Longbowman,
            Healer, Monk, Paladin,
            RoyalGuard, QueenStrategist, KingWarlord
        ]

    def generate_unit_pool(self):
        """
        Generates a pool of units available for purchase.
        """
        unit_pool = []
        for _ in range(10):
            UnitClass = random.choice(self.possible_units)
            faction = UNIT_FACTIONS.get(UnitClass, 'Neutral')
            unit_pool.append(UnitClass(faction))
        return unit_pool

    def get_or_create_shop(self, player_number):
        """
        Gets an existing shop or creates a new one for a player.
        """
        if player_number not in self.player_shops:
            self.player_shops[player_number] = self.generate_unit_pool()
        return self.player_shops[player_number]

    def refresh_shop(self, player_number):
        """
        Refreshes the shop for a specific player.
        """
        self.player_shops[player_number] = self.generate_unit_pool()
        return self.player_shops[player_number]


def buy_units(budget, player_number, player_units, shop):
    """
    Allows a player to buy units within their budget.
    """
    if player_units is None:
        player_units = []

    units = []
    while True:
        unit_pool = shop.get_or_create_shop(player_number)
        print(f"\nPlayer {player_number}, your budget: {budget}")
        print("Available units:")
        for i, unit in enumerate(unit_pool):
            print(f"{i+1}. {unit.name} (Faction: {unit.faction}, Speed: {unit.speed}, Cost: {unit.cost})")

        choice = input("Enter the number of the unit to buy, 'r' to refresh the shop (-1 budget), 'q' to finish buying: ")

        if choice.lower() == 'q':
            break
        elif choice.lower() == 'r':
            if budget < 1:
                print("Not enough budget to refresh the shop.")
                continue
            budget -= 1
            unit_pool = shop.refresh_shop(player_number)
            print("Shop refreshed.")
            continue
        else:
            try:
                index = int(choice) - 1
                if index < 0 or index >= len(unit_pool):
                    print("Invalid choice. Please try again.")
                    continue

                unit = unit_pool[index]
                if budget >= unit.cost:
                    units.append(unit)
                    budget -= unit.cost
                    print(f"Bought {unit.name}. Remaining budget: {budget}")
                else:
                    print("Not enough budget to buy this unit.")
            except ValueError:
                print("Invalid input. Please enter a number, 'r', or 'q'.")

    return units, budget
