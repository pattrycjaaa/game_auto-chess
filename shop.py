# shop.py

import random

from units import (
    Knight, Lancer, ShieldBearer,
    Archer, Crossbowman, Longbowman,
    Healer, Monk, Paladin,
    RoyalGuard, QueenStrategist, KingWarlord
)

def generate_unit_pool():
    """
    Generates a pool of units available for purchase.
    """
    factions = ['Knighthood', 'Royalty', 'Archers', 'Clerics']
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
        faction = random.choice(factions)
        unit_pool.append(UnitClass(faction))
    return unit_pool

def buy_units(budget):
    """
    Allows the player to purchase units from the shop.
    """
    unit_pool = generate_unit_pool()
    purchased_units = []
    refresh_cost = 2  # Cost to refresh the shop

    print("\nAvailable units for purchase:")
    while budget > 0:
        # Display units in the shop
        for i, unit in enumerate(unit_pool):
            print(f"{i + 1}: {unit.name} of {unit.faction} (Cost: {unit.cost}, Health: {unit.health}, "
                  f"Attack: {unit.attack}, Defense: {unit.defense}, Speed: {unit.speed})")
        print(f"0: Finish purchasing units\nr: Refresh shop for {refresh_cost} budget")

        # Get user input and validate
        choice = input(f"\nYour budget: {budget}. Choose a unit to buy (1-{len(unit_pool)}), 'r' to refresh, or 0 to finish: ")

        if choice == "0":
            break
        elif choice.lower() == "r":
            if budget >= refresh_cost:
                budget -= refresh_cost
                unit_pool = generate_unit_pool()  # Refresh the shop
                print("\nShop refreshed!")
            else:
                print("Not enough budget to refresh the shop.")
        else:
            try:
                index = int(choice) - 1
                if 0 <= index < len(unit_pool):
                    unit = unit_pool[index]
                    if budget >= unit.cost:
                        purchased_units.append(unit)
                        budget -= unit.cost
                        print(f"You purchased: {unit.name} of {unit.faction}")
                        # Remove purchased unit from the pool
                        del unit_pool[index]
                    else:
                        print("Not enough budget to buy this unit.")
                else:
                    print("Invalid choice. Please select a valid unit number.")
            except ValueError:
                print("Invalid input. Please enter a number or 'r' to refresh.")

    return purchased_units
