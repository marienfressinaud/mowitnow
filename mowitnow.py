#!/bin/env python3
# encoding: utf-8

import argparse
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the file containing the instructions")
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        print(f"The file {args.filename} does not exist.")
        exit(1)

    with open(args.filename, "r") as f:
        instructions = f.read()

    print(instructions, end="")
