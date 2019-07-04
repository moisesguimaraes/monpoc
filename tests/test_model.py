from monpoc import Agenda, Faction, Ability, ABILITIES, Building, Attack, Unit, Monster
import unittest


# Abilities


class TestAbility(unittest.TestCase):
    def setUp(self):
        self.ability = Ability("Mechanical", "This monster is mechanical.")

    def from_data(self):
        self.assertEqual(
            self.ability,
            Ability.from_data(["Mechanical", "This monster is mechanical."]),
        )

    def test_to_csv(self):
        self.assertEqual(
            self.ability.to_csv(), "Mechanical;This monster is mechanical."
        )


# Buildings


class TestBuilding(unittest.TestCase):
    def setUp(self):
        self.abilities_data = [["Incombustable", 0], ["Opportunity", 0]]

        abilities = [ABILITIES["Incombustable"], ABILITIES["Opportunity"]]
        self.building = Building(
            name="Statue of Liberty", defense=6, abilities=abilities
        )

    def test_from_data(self):
        self.assertEqual(
            self.building,
            Building.from_data(
                [
                    "Statue of Liberty",
                    "",
                    "",
                    "Building",
                    6,
                    [["Incombustable", 0], ["Opportunity", 0]],
                ]
            ),
        )

    def test_to_csv(self):
        self.assertEqual(
            self.building.to_csv(), "Statue of Liberty;6;Incombustable, Opportunity"
        )


# Units


class TestUnit(unittest.TestCase):
    def setUp(self):
        self.unit = Unit(
            name="G-Tank",
            agenda=Agenda.PROTECTORS,
            faction=Faction.GUARD,
            speed=4,
            defense=4,
            brawl=Attack(1, 1, 0),
            blast=Attack(5, 2, 0),
            cost=1,
            abilities=[(ABILITIES["Aim"], 0), (ABILITIES["All Terrain"], 0)],
        )

    def test_from_data(self):
        self.assertEqual(
            self.unit,
            Unit.from_data(
                [
                    "G-Tank",
                    "Protectors",
                    "G.U.A.R.D.",
                    4,
                    4,
                    "1+0",
                    "Rng:5 2+0",
                    "1",
                    [["Aim", 0], ["All Terrain", 0]],
                ]
            ),
        )

    def test_to_csv(self):
        self.assertEqual(
            self.unit.to_csv(),
            "G-Tank;Protectors;G.U.A.R.D.;4;4;0;1;1;0;2;5;1;Aim, All Terrain",
        )


# Monsters


class TestMonster(unittest.TestCase):
    def setUp(self):
        hyper_form = Monster(
            name="Hyper Zor-Raiden",
            agenda=Agenda.PROTECTORS,
            faction=Faction.SHADOW_SUN_SYNDICATE,
            speed=7,
            defense=9,
            brawl=Attack(1, 8, 6),
            blast=Attack(3, 4, 4),
            power=Attack(1, 7, 4),
            health=5,
            abilities=[
                (ABILITIES["Combat Coordination"], 0),
                (ABILITIES["Flank"], 0),
                (ABILITIES["High Mobility"], 0),
                (ABILITIES["Hit & Run"], 1),
                (ABILITIES["Reposition"], 0),
                (ABILITIES["Weapon Master"], 1),
            ],
        )
        self.monster = Monster(
            name="Zor-Raiden",
            agenda=Agenda.PROTECTORS,
            faction=Faction.SHADOW_SUN_SYNDICATE,
            speed=7,
            defense=9,
            brawl=Attack(1, 8, 4),
            blast=Attack(0, 0, 0),
            power=Attack(1, 6, 4),
            health=10,
            abilities=[
                (ABILITIES["Combat Coordination"], 0),
                (ABILITIES["High Mobility"], 0),
                (ABILITIES["Hit & Run"], 1),
                (ABILITIES["Reposition"], 0),
            ],
            hyper_form=hyper_form,
        )

    def test_from_data(self):
        self.assertEqual(
            self.monster,
            Monster.from_data(
                [
                    "Zor-Raiden",
                    "Protectors",
                    "Shadow Sun Syndicate",
                    7,
                    9,
                    "8+4",
                    "-",
                    "6+4",
                    10,
                    [
                        ["Combat Coordination", 0],
                        ["High Mobility", 0],
                        ["Hit & Run", 1],
                        ["Reposition", 0],
                    ],
                    [
                        [
                            "Hyper Zor-Raiden",
                            "Protectors",
                            "Shadow Sun Syndicate",
                            7,
                            9,
                            "8+6",
                            "Rng:3 4+4",
                            "7+4",
                            5,
                            [
                                ["Combat Coordination", 0],
                                ["Flank", 0],
                                ["High Mobility", 0],
                                ["Hit & Run", 1],
                                ["Reposition", 0],
                                ["Weapon Master", 1],
                            ],
                        ]
                    ],
                ]
            ),
        )

    def test_to_csv(self):
        pass
        self.assertEqual(
            self.monster.to_csv(),
            "Zor-Raiden;Protectors;Shadow Sun Syndicate;7;7"
            ";9;9;4;8;1;6;8;1;0;0;0;4;4;3;4;6;1;4;7;1;10;5;Combat Coordination, "
            "High Mobility, Hit & Run - Brawl, Reposition;Combat Coordination, Flank, "
            "High Mobility, Hit & Run - Brawl, Reposition, Weapon Master - Brawl",
        )


if __name__ == "__main__":
    unittest.main()
