from monpoc import Ability, ABILITIES, Building
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
                ["Statue of Liberty", None, None, None, 6, self.abilities_data]
            ),
        )

    def test_to_csv(self):
        self.assertEqual(
            self.building.to_csv(), "Statue of Liberty;6;Incombustable, Opportunity"
        )


# Units


class TestUnit(unittest.TestCase):
    def test_from_data(self):
        pass


# Monsters


class TestMonster(unittest.TestCase):
    def test_from_data(self):
        pass


if __name__ == "__main__":
    unittest.main()
