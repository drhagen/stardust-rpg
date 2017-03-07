from math import sqrt
from unittest import TestCase

from sheet.models.dice import DiceFormula


class StatisticsTestCase(TestCase):
    def test_statistics(self):
        six = DiceFormula.from_str('d6')
        self.assertAlmostEqual(six.mean(), 3.5)
        # Variance from https://stats.stackexchange.com/questions/198025/
        self.assertAlmostEqual(six.std(), sqrt(105 / 36))

        six_plus_one = DiceFormula.from_str('d6 + 1')
        self.assertAlmostEqual(six_plus_one.mean(), 4.5)
        self.assertAlmostEqual(six_plus_one.std(), sqrt(105 / 36))

        four_sixes = DiceFormula.from_str('2d6 + d6 + d6')
        self.assertAlmostEqual(four_sixes.mean(), 4 * 3.5)
        self.assertAlmostEqual(four_sixes.std(), 2 * sqrt(105 / 36))
