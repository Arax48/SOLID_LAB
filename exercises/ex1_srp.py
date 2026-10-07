"""
Exercise 1 - Single Responsibility Principle (SRP)

PROBLEM: the Car class below does three unrelated jobs at once:
  1. Tracks its own race state (name, speed, position).
  2. Prints its own status line to the console on every move.
  3. Appends a line to a results log on disk on every move.

That is three different reasons for Car to change (a new state field, a
new print format, a new log format) -- exactly what SRP says a class
should not have.

YOUR TASK:
  1. Strip Car down so it ONLY tracks state and knows how to move itself.
     Remove the print() and the file-writing from move().
  2. Write a new `RaceLogger` class, responsible for recording race
     results and saving them to disk, completely independent of Car:
       - record(tick, racers): remember each racer's position for this tick
       - save(path="race_log.txt"): write everything recorded so far to disk
       - an `entries` property returning the recorded entries as a list of str
  3. Wire it together in main(): pass `logger.record` as the `on_tick`
     callback to `Track.run(...)`, then call `logger.save()` once the
     race finishes.

Run it to see (and hear silence from) your fix:
    python -m exercises.ex1_srp

Check your work:
    pytest tests/test_ex1_srp.py -v
"""
from engine.track import Track


class Car:
    def __init__(self, name: str, speed: int, symbol: str = "\U0001F697"):
        self.name = name
        self.speed = speed
        self.symbol = symbol
        self.position = 0

    def move(self) -> None:
        # Car solo se encarga de su propio estado/movimiento.
        self.position += self.speed


class RaceLogger:
    def __init__(self) -> None:
        self._entries: list[str] = []

    def record(self, tick: int, racers: list[Car]) -> None:
        """Registra la posición de todos los vehículos en un tick."""
        snapshot = ", ".join(
            f"{racer.name}={racer.position}" for racer in racers
        )
        self._entries.append(f"tick {tick}: {snapshot}")

    @property
    def entries(self) -> list[str]:
        """Devuelve las entradas registradas."""
        return list(self._entries)

    def save(self, path: str = "race_log.txt") -> None:
        """Guarda todo lo registrado hasta ahora en disco."""
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self._entries))


def main():
    cars = [Car("Red", 4), Car("Blue", 5), Car("Green", 3)]

    logger = RaceLogger()
    track = Track(length=30)

    track.run(cars, on_tick=logger.record)
    logger.save()


if __name__ == "__main__":
    main()