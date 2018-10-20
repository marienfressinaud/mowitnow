#!/bin/env python3
# encoding: utf-8

import argparse
import os

from enum import Enum


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @classmethod
    def from_abbr(cls, abbr):
        try:
            value = ["N", "E", "S", "W"].index(abbr)
            return cls(value)
        except ValueError:
            raise ValueError(f"{abbr} must be part of N, E, S or W")

    def left(self):
        return self.__class__((self.value - 1) % 4)

    def right(self):
        return self.__class__((self.value + 1) % 4)

    def abbr(self):
        return ["N", "E", "S", "W"][self.value]


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def contained_in(self, size):
        if 0 <= self.x and self.x <= size[0] and 0 <= self.y and self.y <= size[1]:
            return True
        return False

    def move(self, direction):
        if direction is Direction.NORTH:
            return Position(self.x, self.y + 1)
        elif direction is Direction.SOUTH:
            return Position(self.x, self.y - 1)
        elif direction is Direction.WEST:
            return Position(self.x - 1, self.y)
        elif direction is Direction.EAST:
            return Position(self.x + 1, self.y)
        else:
            return self

    def __str__(self):
        return f"({self.x}, {self.y})"


def get_lawn_size(instruction):
    """Return the size of the lawn from an instruction.

    Examples:

    >>> get_lawn_size("5 5")
    (5, 5)

    >>> get_lawn_size("0 0") is None
    True

    >>> get_lawn_size("-5 5") is None
    True

    >>> get_lawn_size("5 -5") is None
    True

    >>> get_lawn_size("5 5 5") is None
    True

    >>> get_lawn_size("5") is None
    True

    >>> get_lawn_size("") is None
    True

    >>> get_lawn_size("foo bar") is None
    True
    """
    try:
        size = tuple(int(x) for x in instruction.split(" "))
    except ValueError:
        return None

    if len(size) != 2:
        return None

    if size[0] <= 0 or size[1] <= 0:
        return None

    return size


def init_mower(instruction, lawn_size):
    """Return a mower initialized from instruction.

    Examples:

    >>> lawn_size = (5, 5)
    >>> init_mower("1 2 N", lawn_size) # doctest: +ELLIPSIS
    (<mowitnow.Position ...>, <Direction.NORTH: 0>)

    >>> init_mower("5 5 S", lawn_size) # doctest: +ELLIPSIS
    (<mowitnow.Position ...>, <Direction.SOUTH: 2>)

    >>> init_mower("", lawn_size) is None
    True

    >>> init_mower("1", lawn_size) is None
    True

    >>> init_mower("1 N 2", lawn_size) is None
    True

    >>> init_mower("N 1 2", lawn_size) is None
    True

    >>> init_mower("1 2 N S", lawn_size) is None
    True

    >>> init_mower("1 2 A", lawn_size) is None
    True

    >>> init_mower("-1 2 N", lawn_size) is None
    True

    >>> init_mower("1 6 N", lawn_size) is None
    True
    """
    items = instruction.split(" ")
    if len(items) != 3:
        return None

    try:
        position = Position(int(items[0]), int(items[1]))
        direction = Direction.from_abbr(items[2])
    except ValueError:
        return None

    if not position.contained_in(lawn_size):
        return None

    return (position, direction)


def move_mower(mower, movement, lawn_size):
    """Move a mower from instruction.

    Examples:

    >>> lawn_size = (5, 5)
    >>> mower = (Position(1, 2), Direction.from_abbr("N"))

    >>> position, direction = move_mower(mower, "G", lawn_size)
    >>> str(position)
    '(1, 2)'
    >>> direction
    <Direction.WEST: 3>

    >>> position, direction = move_mower(mower, "D", lawn_size)
    >>> str(position)
    '(1, 2)'
    >>> direction
    <Direction.EAST: 1>

    >>> position, direction = move_mower(mower, "A", lawn_size)
    >>> str(position)
    '(1, 3)'
    >>> direction
    <Direction.NORTH: 0>

    >>> position, direction = move_mower(mower, "P", lawn_size)
    >>> str(position)
    '(1, 2)'
    >>> direction
    <Direction.NORTH: 0>

    >>> position, direction = move_mower(mower, "", lawn_size)
    >>> str(position)
    '(1, 2)'
    >>> direction
    <Direction.NORTH: 0>

    >>> mower = (Position(5, 5), Direction.from_abbr("N"))
    >>> position = move_mower(mower, "A", lawn_size)[0]
    >>> str(position)
    '(5, 5)'

    >>> mower = (Position(5, 5), Direction.from_abbr("E"))
    >>> position = move_mower(mower, "A", lawn_size)[0]
    >>> str(position)
    '(5, 5)'

    >>> mower = (Position(0, 0), Direction.from_abbr("S"))
    >>> position = move_mower(mower, "A", lawn_size)[0]
    >>> str(position)
    '(0, 0)'

    >>> mower = (Position(0, 0), Direction.from_abbr("W"))
    >>> position = move_mower(mower, "A", lawn_size)[0]
    >>> str(position)
    '(0, 0)'
    """
    if movement == "G":
        return (mower[0], mower[1].left())
    if movement == "D":
        return (mower[0], mower[1].right())
    elif movement == "A":
        new_position = mower[0].move(mower[1])
        if not new_position.contained_in(lawn_size):
            return mower
        return (new_position, mower[1])

    return mower


def instructions_from_file(filename):
    if not os.path.exists(filename):
        return None

    with open(filename, "r") as f:
        return f.read().splitlines()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the file containing the instructions")
    args = parser.parse_args()

    instructions = instructions_from_file(args.filename)
    if instructions is None:
        print(f"The file {args.filename} does not exist.")
        exit(1)

    if len(instructions) == 1:
        print("Instructions for mowers are missing.")
        exit(1)

    if len(instructions) % 2 != 1:
        # Note that we are looking for an odd number because the first line is
        # for lawn size.
        print("Each mower instructions must be on 2 lines.")
        exit(1)

    lawn_size = get_lawn_size(instructions[0])
    if lawn_size is None:
        print("The lawn width and height must be greater than 0.")
        exit(1)

    number_of_mowers = (len(instructions) - 1) // 2
    for mower_number in range(1, number_of_mowers + 1):
        mower = init_mower(instructions[(mower_number * 2) - 1], lawn_size)
        if mower is None:
            print(f"Instructions to init mower #{mower_number} are not valid.")
            exit(1)

        for movement in instructions[mower_number * 2]:
            mower = move_mower(mower, movement, lawn_size)

        print(f"{mower[0].x} {mower[0].y} {mower[1].abbr()}")
