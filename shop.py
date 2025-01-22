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
        self.player_shops = {}
        self.possible_units = [
            Knight, Lancer, ShieldBearer,
            Archer, Crossbowman, Longbowman,
            Healer, Monk, Paladin,
            RoyalGuard, QueenStrategist, KingWarlord
        ]

    def generate_unit_pool(self):
        """
        Generates a pool of 10 units available for purchase.
        """
        unit_pool = []
        for _ in range(10):
            UnitClass = random.choice(self.possible_units)
            faction = UNIT_FACTIONS.get(UnitClass, 'Neutral')
            unit_pool.append(UnitClass(faction))
        return unit_pool

    def get_or_create_shop(self, player_number):
        """
        (Nieużywane w tej wersji – można usunąć lub zostawić)
        """
        if player_number not in self.player_shops:
            self.player_shops[player_number] = self.generate_unit_pool()
        return self.player_shops[player_number]

    def refresh_shop(self, player_number):
        """
        (Nieużywane w tej wersji – można usunąć lub zostawić)
        """
        self.player_shops[player_number] = self.generate_unit_pool()
        return self.player_shops[player_number]


def buy_units(budget, player_number, player_units, shop):
    """
    Pozwala graczowi kupować jednostki w pętli:
     - Za każdym razem losuje nową 10-elementową pulę (shop.generate_unit_pool()).
     - Gracz kupuje (lub nie) 1 jednostkę.
     - Po zakupie wraca do pętli -> Znowu nowa pula.

    Parametry:
      - budget: obecny budżet gracza
      - player_number: np. 1 (lub cokolwiek)
      - player_units: lista jednostek, które gracz posiada (jeśli None, tworzymy pustą)
      - shop: instancja klasy Shop()

    Zwraca:
      - (units, new_budget) – listę nowo kupionych jednostek + zaktualizowany budżet
    """
    if player_units is None:
        player_units = []

    units = []
    
    while True:
        # 1. Za każdym razem LOSUJEMY nową pulę 10
        unit_pool = shop.generate_unit_pool()
        
        # 2. Filtrujemy jednostki, na które gracza stać
        affordable_units = [u for u in unit_pool if u.cost <= budget]
        if not affordable_units:
            print(f"Player {player_number}, you cannot afford any new unit. Budget: {budget}")
            break
        
        # 3. Wyświetlamy powstałą pulę
        print(f"\nPlayer {player_number}, your budget: {budget}")
        print("Newly generated shop pool (10 units):")
        for i, unit in enumerate(unit_pool):
            print(f"{i+1}. {unit.name} (Faction: {unit.faction}, "
                  f"Speed: {unit.speed}, Cost: {unit.cost})")

        # 4. Zapytaj, czy kupić, czy wyjść
        choice = input("Enter the number of the unit to buy or 'q' to finish buying: ")
        if choice.lower() == 'q':
            break

        try:
            index = int(choice) - 1
            if index < 0 or index >= len(unit_pool):
                print("Invalid choice. Please try again.")
                continue

            chosen_unit = unit_pool[index]
            if chosen_unit.cost > budget:
                print("Not enough budget to buy this unit.")
                continue

            # 5. Kupujemy (dodajemy do tymczasowej listy, odejmujemy budżet)
            units.append(chosen_unit)
            budget -= chosen_unit.cost
            print(f"You bought {chosen_unit.name}. Remaining budget: {budget}")

            # Pętla się NIE kończy – wraca do 'while True',
            # generuje nową pulę, itd.
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")

    return units, budget
