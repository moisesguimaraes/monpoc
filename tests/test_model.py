from monpoc import Ability, ABILITIES, Building
import unittest


# Abilities


class TestAbility(unittest.TestCase):
    def setUp(self):
        self.foo = Ability("foo", "bar")

    def from_data(self):
        self.assertEqual(self.foo, Ability.from_data(["foo", "bar"]))

    def test_to_csv(self):
        self.assertEqual(self.foo.to_csv(), "foo; bar\n")


# Buildings


class TestBuilding(unittest.TestCase):
    def setUp(self):
        self.ab_data = [["Incombustable", 0], ["Opportunity", 0]]

        ab = [ABILITIES["Incombustable"], ABILITIES["Opportunity"]]
        self.lib = Building(name="Statue of Liberty", defense=6, abilities=ab)

    def test_from_data(self):
        self.assertEqual(
            self.lib,
            Building.from_data(
                ["Statue of Liberty", None, None, None, 6, self.ab_data]
            ),
        )

    def test_to_csv(self):
        self.assertEqual(
            self.lib.to_csv(), "Statue of Liberty; 6; Incombustable, Opportunity\n"
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
