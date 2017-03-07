import re

from typing import Tuple
from math import sqrt

class Dice:
    def __init__(self, sides: int, num_dice: int = 1) -> None:
        self.sides = sides
        self.num_dice = num_dice

    @classmethod
    def from_str(cls, dice_string: str) -> 'Dice':
        # Examples: d4 2d10 d20 10d20
        match = re.fullmatch(r'^(?P<num_dice>\d*)d(?P<sides>\d+)?', dice_string)

        if match is not None:
            sides = int(match.group('sides'))
            num_dice = match.group('num_dice')
            if num_dice != '':
                return cls(sides=sides, num_dice=int(num_dice))
            else:
                return cls(sides=sides)

    def __str__(self) -> str:
        if self.num_dice > 1:
            num_dice_char = str(self.num_dice)
        else:
            num_dice_char = ''
        return f'{num_dice_char}d{self.sides}'


class DiceFormula:
    def __init__(self, dice_pool: Tuple[Dice, ...], modifier: int = 0) -> None:
        self.dice_pool = dice_pool
        self.modifier = modifier

    @classmethod
    def from_str(cls, formula_string: str) -> 'DiceFormula':
        # Examples: 'd4' 'd4 + d6' 'd4 + 2d4 + 1'
        dice_pool = []
        modifier = None
        for token in formula_string.split():
            if token == '+':
                continue
            elif 'd' in token:
                dice_pool.append(Dice.from_str(token))
            elif modifier is None:
                modifier = int(token)
            else:
                raise ValueError(f'Invald token: {token}')

        if modifier is None:
            return cls(dice_pool=tuple(dice_pool))
        else:
            return cls(dice_pool=tuple(dice_pool), modifier=modifier)

    # The average value of a roll
    def mean(self):
        sum = self.modifier
        for die in self.dice_pool:
            sum += die.num_dice * (die.sides + 1) / 2

        return sum

    # The standard deviation of a roll
    def std(self):
        var = 0
        for die in self.dice_pool:
            var += die.num_dice * (die.sides ** 2 - 1) / 12

        return sqrt(var)

    def __str__(self) -> str:
        s = ''
        for dice in self.dice_pool:
            s += f'{dice} + '

        if self.modifier > 0:
            s += str(self.modifier)
        else:
            s = s[:-len(' + ')]

        return s
