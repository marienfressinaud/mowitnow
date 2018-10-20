#!/bin/env python3
# encoding: utf-8

import argparse
import os

from enum import Enum


class Direction(Enum):
    NORTH = "N"
    EAST = "E"
    WEST = "W"
    SOUTH = "S"


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def contained_in(self, size):
        if 0 <= self.x and self.x <= size[0] and 0 <= self.y and self.y <= size[1]:
            return True
        return False

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
    (<mowitnow.Position ...>, <Direction.NORTH: 'N'>)

    >>> init_mower("5 5 S", lawn_size) # doctest: +ELLIPSIS
    (<mowitnow.Position ...>, <Direction.SOUTH: 'S'>)

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
        direction = Direction(items[2])
    except ValueError:
        return None

    if not position.contained_in(lawn_size):
        return None

    return (position, direction)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the file containing the instructions")
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        print(f"The file {args.filename} does not exist.")
        exit(1)

    with open(args.filename, "r") as f:
        instructions = f.read()

    instruction_lines = instructions.splitlines()

    if len(instruction_lines) == 1:
        print("Instructions for mowers are missing.")
        exit(1)

    if len(instruction_lines) % 2 != 1:
        # Note that we are looking for an odd number because the first line is
        # for lawn size.
        print("Each mower instructions must be on 2 lines.")
        exit(1)

    lawn_size = get_lawn_size(instruction_lines[0])
    if lawn_size is None:
        print("The lawn width and height must be greater than 0.")
        exit(1)

    print(f"Lawn size is {lawn_size[0]}x{lawn_size[1]}.")

    number_of_mowers = (len(instruction_lines) - 1) // 2
    for mower_number in range(1, number_of_mowers + 1):
        mower = init_mower(instruction_lines[(mower_number * 2) - 1], lawn_size)
        if mower is None:
            print(f"Instructions to init mower #{mower_number} are not valid.")
            exit(1)

        print(f"Mower #{mower_number}: {mower[0]} {mower[1].name}")
