from dataclasses import dataclass, field
from typing import Type, List
from enum import Enum
import itertools

from monpoc.game_data import DATA as _DATA


_AGENDAS = {1: ["Protectors", "PROTECTORS"], 2: ["Destroyers", "DESTROYERS"]}

Agenda = Enum(
    value="Agenda",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _AGENDAS.items()
    ),
)

_FACTIONS = {
    1: ["G.U.A.R.D.", "GUARD"],
    2: ["Shadow Sun Syndicate", "SHADOW_SUN_SYNDICATE"],
    3: ["Terrasaurs", "TERRASAURS"],
    4: ["Lords of Cthul", "LORDS_OF_CTHUL"],
    5: ["Martian Menace", "MARTIAN_MENACE"],
    6: ["Planet Eaters", "PLANET_EATERS"],
    7: ["Tritons", "TRITONS"],
    8: ["Subterran Uprising", "SUBTERRAN_UPRISING"],
    9: ["Empire of the Apes", "APES"],
    10: ["UberCorp International", "UBERCORP"],
    11: ["Green Fury", "GREEN_FURY"],
}

Faction = Enum(
    value="Faction",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _FACTIONS.items()
    ),
)


@dataclass
class Attack:
    reach: int = 0
    action: int = 0
    booster: int = 0

    @classmethod
    def from_data(cls, data):
        if data == "-":
            return cls()

        if data.startswith("Rng:"):
            data = data[4:]
        else:
            data = "1 " + data

        return cls(*[int(d) for d in data.replace("+", " ").split()])

    def __str__(self):
        if self.reach == 0:
            return ""

        if self.reach == 1:
            return f"{self.action}+{self.booster}"

        return f"Rng:{self.reach} {self.action}+{self.booster}"

    def to_csv(self):
        return f"{self.booster};{self.action};{self.reach}"

    def rating(self):
        return self.booster * 100 + self.action * 10 + self.reach


@dataclass
class Ability:
    name: str
    descryption: str

    @classmethod
    def from_data(cls, data):
        return cls(data[0], data[1])

    @staticmethod
    def scope(n):
        s = {0: "", 1: " - Brawl", 2: " - Blast", 3: " - Power"}

        return s[n]

    @staticmethod
    def csv_headers():
        return "Name;Description"

    def to_csv(self):
        return f"{self.name};{self.descryption}"


ABILITIES = {d[0]: Ability.from_data(d) for d in _DATA["abilities"]}


@dataclass
class Model:
    name: str = ""
    agenda: Agenda = None
    faction: Faction = None
    defense: int = 0
    health: int = 1
    abilities: List[Ability] = field(default_factory=list)


@dataclass
class Building:
    name: str = ""
    defense: int = 0
    abilities: List[Ability] = field(default_factory=list)

    @classmethod
    def from_data(cls, data):
        abilities = [ABILITIES[a[0]] for a in data[5]]

        return cls(name=data[0], defense=int(data[4]), abilities=abilities)

    @staticmethod
    def csv_headers():
        return "Name;Defense;Abilities"

    def to_csv(self):
        return (
            f"{self.name};{self.defense};"
            f"{', '.join([_.name for _ in self.abilities])}"
        )


BUILDINGS = {d[0]: Building.from_data(d) for d in _DATA["buildings"]}


@dataclass
class Unit(Model):
    speed: int = 0
    brawl: Attack = None
    blast: Attack = None
    cost: int = 0

    @classmethod
    def from_data(cls, data):
        abilities = [(ABILITIES[a[0]], a[1]) for a in data[8]]

        return Unit(
            name=data[0],
            agenda=Agenda[data[1]],
            faction=Faction[data[2]],
            speed=int(data[3]),
            defense=int(data[4]),
            brawl=Attack.from_data(data[5]),
            blast=Attack.from_data(data[6]),
            cost=int(data[7]),
            abilities=abilities,
        )

    @staticmethod
    def csv_headers():
        return "Name;Agenda;Faction;Speed;Defense;Brawl;;;Blast;;;Cost;Abilities"

    def to_csv(self):
        return (
            f"{self.name};{self.agenda.name};{self.faction.name};{self.speed};"
            f"{self.defense};{self.brawl.to_csv()};{self.blast.to_csv()};{self.cost};"
            f"{', '.join([_[0].name + Ability.scope(_[1]) for _ in self.abilities])}"
        )


UNITS = {d[0]: Unit.from_data(d) for d in _DATA["units"]}


@dataclass
class Monster(Unit):
    power: Attack = None
    hyper_form: Type["Monster"] = None

    @classmethod
    def from_data(cls, data):
        abilities = [(ABILITIES[a[0]], a[1]) for a in data[9]]

        hyper_form = Monster.from_data(data[10][0]) if len(data) > 10 else None

        return Monster(
            name=data[0],
            agenda=Agenda[data[1]],
            faction=Faction[data[2]],
            speed=int(data[3]),
            defense=int(data[4]),
            brawl=Attack.from_data(data[5]),
            blast=Attack.from_data(data[6]),
            power=Attack.from_data(data[7]),
            health=int(data[8]),
            abilities=abilities,
            hyper_form=hyper_form,
        )

    @staticmethod
    def csv_headers():
        return (
            "Name;Agenda;Faction;Speed;Hyper Speed;Defense;Hyper Defense;"
            "Brawl;;;Hyper Brawl;;;Blast;;;Hyper Blast;;;Power;;;Hyper Power;;;"
            "Health;Hyper Health;Abilities;Hyper Abilities"
        )

    def to_csv(self):
        hyper = self.hyper_form if self.hyper_form else self

        return (
            f"{self.name};{self.agenda.name};{self.faction.name};{self.speed};"
            f"{hyper.speed};{self.defense};{hyper.defense};{self.brawl.to_csv()};"
            f"{hyper.brawl.to_csv()};{self.blast.to_csv()};{hyper.blast.to_csv()};"
            f"{self.power.to_csv()};{hyper.power.to_csv()};{self.health};{hyper.health};"
            f"{', '.join([_[0].name + Ability.scope(_[1]) for _ in self.abilities])};"
            f"{', '.join([_[0].name + Ability.scope(_[1]) for _ in hyper.abilities])}"
        )


MONSTERS = {d[0]: Monster.from_data(d) for d in _DATA["monsters"]}
