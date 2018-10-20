#!/bin/env python3
# encoding: utf-8

import argparse
import os


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

    lawn_size = get_lawn_size(instruction_lines[0])
    if lawn_size is None:
        print("The lawn width and height must be greater than 0.")
        exit(1)

    print(f"Lawn size is {lawn_size[0]}x{lawn_size[1]}.")
