from monpoc import Agenda, Faction, Ability, ABILITIES, Building, Attack, Unit
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
        self.building = Building(name="Statue of Liberty", defense=6, abilities=abilities)

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
                    ],
            ),
        )

    def test_to_csv(self):
        self.assertEqual(
            self.building.to_csv(), "Statue of Liberty;6;Incombustable, Opportunity"
        )


# Units


class TestUnit(unittest.TestCase):
    def setUp(self):
        self.unit = Unit(name="G-Tank", agenda=Agenda.PROTECTORS, faction=Faction.GUARD,
                         speed=4, defense=4, brawl=Attack(1, 1, 0), blast=Attack(5, 2, 0),
                         cost=1, abilities=[ABILITIES["Aim"], ABILITIES["All Terrain"]])

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
            "G-Tank;Protectors;G.U.A.R.D.;4;4;1+0;Rng:5 2+0;1;Aim, All Terrain"
        )


# Monsters


class TestMonster(unittest.TestCase):
    def test_from_data(self):
        pass


if __name__ == "__main__":
    unittest.main()
