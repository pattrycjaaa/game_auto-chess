# ai_player.py

from shop import Shop

class AIPlayer:
    """
    AI, które:
      1) Przy każdej pojedynczej transakcji generuje NOWĄ pulę 10 jednostek.
      2) Wybiera frakcję, której ma najwięcej w `self.units` (synergy_faction).
      3) Kupuje najlepszą jednostkę synergy_faction (o najwyższym (attack, speed)) 
         jeśli jest w budżecie i występuje w puli.
      4) W przeciwnym razie kupuje najlepszą spoza synergy_faction.
    """
    def __init__(self, budget):
        self.name = "AI Player"
        self.health = 100
        self.budget = budget
        self.units = []
        self.shop = Shop()

    def buy_units(self):
        """
        Pętla: dopóki AI ma budżet > 0:
          - generuje NOWĄ pulę 10
          - oblicza synergy_faction (najczęstsza frakcja w self.units)
          - kupuje jedną kartę (jeśli się da)
          - powtarza
        """
        print(f"AI (budget={self.budget}) starts buying units...")

        while True:
            if self.budget <= 0:
                print("AI has no budget left.")
                break

            # Każda transakcja = nowe 10
            unit_pool = self.shop.generate_unit_pool()

            synergy_faction = self._get_synergy_faction()

            # Filtrujemy, co jest w zasięgu budżetu
            affordable_units = [u for u in unit_pool if u.cost <= self.budget]
            if not affordable_units:
                print("AI can't afford any unit from the new pool.")
                break

            # Wybieramy w pierwszej kolejności synergy_faction
            synergy_units = [u for u in affordable_units if u.faction == synergy_faction]
            if synergy_units:
                unit_to_buy = max(synergy_units, key=lambda u: (u.attack, u.speed))
            else:
                unit_to_buy = max(affordable_units, key=lambda u: (u.attack, u.speed))

            # Kupujemy jedną jednostkę
            self.units.append(unit_to_buy)
            self.budget -= unit_to_buy.cost
            print(f"AI purchased {unit_to_buy.name} (Faction: {unit_to_buy.faction}, "
                  f"Attack: {unit_to_buy.attack}, Speed: {unit_to_buy.speed}, "
                  f"Cost: {unit_to_buy.cost}). Budget left: {self.budget}")

        print(f"AI has {len(self.units)} units after purchasing. Final budget: {self.budget}")


    def _get_synergy_faction(self):
        """
        Zwraca frakcję, której AI ma najwięcej w `self.units`.
        Jeśli AI nie ma żadnej jednostki, zwróci None.
        """
        if not self.units:
            return None

        faction_counts = {}
        for unit in self.units:
            faction_counts[unit.faction] = faction_counts.get(unit.faction, 0) + 1

        synergy_faction = max(faction_counts, key=faction_counts.get)
        return synergy_faction

    def choose_attack_order(self):
        """
        Sortuje żywe jednostki malejąco po speed (do fazy ataku).
        """
        self.units = sorted(
            [unit for unit in self.units if unit.is_alive()],
            key=lambda u: -u.speed
        )
        print("AI attack order determined:")
        for unit in self.units:
            print(f"  {unit.name} (Speed: {unit.speed})")
        return self.units
