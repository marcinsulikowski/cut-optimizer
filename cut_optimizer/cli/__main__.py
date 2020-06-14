"""CLI for the cut optimizer."""

import argparse
import sys
from typing import List, TextIO

from cut_optimizer.algorithms.optimize_x_moves import optimize_x_moves
from cut_optimizer.instance import Point, Polyline


def read_instance(input_file: TextIO) -> List[Polyline]:
    """Read CutInstance from an I/O stream."""
    polylines = []
    for line in input_file:
        if not line or line.startswith("#"):
            continue
        tokens = line.split()
        assert len(tokens) == 6
        polylines.append(
            Polyline(
                name=tokens[0],
                start=Point(int(tokens[1]), int(tokens[2])),
                end=Point(int(tokens[3]), int(tokens[4])),
                is_closed={"O": False, "C": True}[tokens[5]],
            )
        )
    return polylines


def main() -> None:
    """Main entry point of the program."""

    parser = argparse.ArgumentParser("X-move optimizer")
    parser.add_argument("input_file", default="-", help="Input file")
    args = parser.parse_args()

    if args.input_file == "-":
        polys = read_instance(sys.stdin)
    else:
        with open(args.input_file, "r") as input_file:
            polys = read_instance(input_file)

    for poly in optimize_x_moves(polys):
        print(poly.name)


if __name__ == "__main__":
    main()
