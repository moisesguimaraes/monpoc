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
    3: ["Terrasaurus", "TERRASAURUS"],
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

        return cls(name=data[0], defense=data[4], abilities=abilities)

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
    power: Attack = None

    @classmethod
    def from_data(cls, data):
        pass


@dataclass
class Monster(Unit):
    hyper_speed: int = 0
    hyper_defense: int = 0
    hyper_abilities: List[Ability] = field(default_factory=list)
