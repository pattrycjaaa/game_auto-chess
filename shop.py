import random

from units.archers import Archer, Crossbowman, Longbowman
from units.clerics import Healer, Monk, Paladin
from units.knighthood import Knight, Lancer, ShieldBearer
from units.royalty import RoyalGuard, QueenStrategist, KingWarlord

# Define a mapping from unit classes to their respective factions
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

def generate_unit_pool():
    """
    Generates a pool of units available for purchase.
    """
    possible_units = [
        Knight,
        Lancer,
        ShieldBearer,
        Archer,
        Crossbowman,
        Longbowman,
        Healer,
        Monk,
        Paladin,
        RoyalGuard,
        QueenStrategist,
        KingWarlord
    ]
    unit_pool = []
    for _ in range(10):
        UnitClass = random.choice(possible_units)
        faction = UNIT_FACTIONS.get(UnitClass, 'Neutral')  # Default to 'Neutral' if not found
        unit_pool.append(UnitClass(faction))  # Assign the correct faction
    return unit_pool

def buy_units(budget, player_number, player_units):
    """
    Allows a player to buy units within their budget.
    """

    if player_units is None:
        player_units = []

    units = []
    while True:
        unit_pool = generate_unit_pool()
        print(f"\nPlayer {player_number}, your budget: {budget}")
        print("Available units:")
        for i, unit in enumerate(unit_pool):
            status = "Dead" if not unit.is_alive() else f"Health: {unit.health}/{unit.max_health}"
            print(f"{i+1}. {unit.name} (Faction: {unit.faction}, Speed: {unit.speed}, Cost: {unit.cost})")
        choice = input("Enter the number of the unit to buy, 'r' to refresh the shop (-1 budget), 'q' to finish buying: ")
        if choice.lower() == 'q':
            break
        elif choice.lower() == 'r':
            budget -= 1  # Cost to refresh the shop
            if budget < 0:
                print("Not enough budget to refresh the shop.")
                budget += 1
                continue
            else:
                print("Shop refreshed.")
                continue
        else:
            try:
                index = int(choice) - 1
                if index < 0 or index >= len(unit_pool):
                    print("Invalid choice. Please try again.")
                    continue
                unit = unit_pool[index]
                living_units = [unit for unit in player_units if unit.is_alive()]
                if len(living_units) >= 6:
                    print("You already have the maximum number of units (6).")
                    continue
                if budget >= unit.cost:
                    units.append(unit)
                    budget -= unit.cost
                    print(f"Bought {unit.name}. Remaining budget: {budget}")
                    player_units.append(unit)
                else:
                    print("Not enough budget to buy this unit.")
            except ValueError:
                print("Invalid input. Please enter a number, 'r', or 'q'.")
    return units, budget