"""
Exercise 5 - Dependency Inversion Principle (DIP)

Race below is a high-level policy ("how to run a race") that is hard-
wired to two concrete, low-level vehicle classes: it builds its own
SportsCar and DeliveryVan inside __init__. Racing a different roster
today means editing Race itself -- exactly what DIP says we should
avoid.

YOUR TASK:
  1. Refactor Race so it receives its racers through the constructor
     (store them as `self.racers`) instead of creating them itself.
     Race must not import or know about SportsCar/DeliveryVan/RocketSled
     at all -- any object satisfying the Racer contract from
     `engine.track` (name, symbol, position, move()) should work.
  2. Add a `RocketSled` vehicle class (any speed you like).
  3. In main(), build two different rosters and run Race with each,
     proving you never had to touch Race to change who races.

Run it to see the race(s):
    python -m exercises.ex5_dip

Check your work:
    pytest tests/test_ex5_dip.py -v
"""

from engine.track import Track


class SportsCar:
    symbol = "\U0001F3CE"

    def __init__(self, name):
        self.name = name
        self.position = 0

    def move(self):
        self.position += 6


class DeliveryVan:
    symbol = "\U0001F690"

    def __init__(self, name):
        self.name = name
        self.position = 0

    def move(self):
        self.position += 3


class RocketSled:
    symbol = "\U0001F680"  # 🚀

    def __init__(self, name):
        self.name = name
        self.position = 0

    def move(self):
        self.position += 9


class Race:
    """High-level policy: run a race with whatever racers are injected."""

    def __init__(self, racers, track=None):
        self.racers = racers
        self.track = track if track is not None else Track(length=30)

    def start(self):
        return self.track.run(self.racers)


def main():
    roster_a = [
        SportsCar("Flash"),
        DeliveryVan("Steady Eddie"),
    ]
    Race(roster_a).start()

    roster_b = [
        RocketSled("Comet"),
        DeliveryVan("Steady Eddie II"),
    ]
    Race(roster_b).start()


if __name__ == "__main__":
    main()
