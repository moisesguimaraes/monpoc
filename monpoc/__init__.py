from dataclasses import dataclass, field
from typing import List
from enum import Enum
import itertools

from monpoc import game_data


_AGENDAS = {1: ["Protectors", "PROTECTORS"], 2: ["Destroyers", "DESTROYERS"]}

Agenda = Enum(
    value="Agenda",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _AGENDAS.items()
    ),
)

_FACTIONS = {
    1: ["G.U.A.R.D.", "GUARD"],
    2: ["Shadow Sun Syndicate", "SHADOW_SUN_S"],
    3: ["Terrasaurs", "TERRASAURS"],
    4: ["Tritons", "TRITONS"],
    5: ["Lords of Cthul", "L_OF_CTHUL"],
    6: ["Martian Menace", "MARTIAN_M"],
    7: ["Planet Eaters", "P_EATERS"],
    8: ["Subterran Uprising", "SUBTERRAN_U"],
}

Faction = Enum(
    value="Faction",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _FACTIONS.items()
    ),
)


@dataclass(order=True)
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


@dataclass
class Ability:
    name: str
    descryption: str

    @classmethod
    def from_data(cls, data):
        return cls(data[0], data[1])

    @staticmethod
    def csv_headers():
        return "Name;Description"

    def to_csv(self):
        return f"{self.name};{self.descryption}"


ABILITIES = {d[0]: Ability.from_data(d) for d in game_data.ABILITIES_DATA}


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
        result = f"{self.name};{self.defense};"
        result += f"{', '.join([_.name for _ in self.abilities])}"

        return result


BUILDINGS = {d[0]: Building.from_data(d) for d in game_data.BUILDINGS_DATA}


@dataclass
class Unit(Model):
    speed: int = 0
    brawl: Attack = None
    blast: Attack = None
    cost: int = 0

    @classmethod
    def from_data(cls, data):
        abilities = [ABILITIES[a[0]] for a in data[8]]

        return Unit(
            name=data[0],
            agenda=Agenda[data[1]],
            faction=Faction[data[2]],
            speed=int(data[3]),
            defense=int(data[4]),
            brawl=Attack.from_data(data[5]),
            blast=Attack.from_data(data[6]),
            cost=int(data[7]),
            abilities=abilities
        )

    @staticmethod
    def csv_headers():
        return "Name;Agenda;Faction;Speed;Defense;Brawl;Blast;Cost;Abilities"

    def to_csv(self):
        result = f"{self.name};{self.agenda.name};{self.faction.name};{self.speed};"
        result += f"{self.defense};{self.brawl};{self.blast};{self.cost};"
        result += f"{', '.join([_.name for _ in self.abilities])}"

        return result


UNITS = {d[0]: Unit.from_data(d) for d in game_data.UNITS_DATA}


@dataclass
class Monster(Unit):
    power: Attack = None
    hyper_speed: int = 0
    hyper_defense: int = 0
    hyper_abilities: List[Ability] = field(default_factory=list)
