"""CLI for the cut optimizer."""

import sys
from typing import TextIO

from cut_optimizer.instance import CutInstance, Polyline, Point


def read_instance(input_file: TextIO) -> CutInstance:
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
    return CutInstance(polylines)


def main() -> None:
    """Main entry point of the program."""
    cut_instance = read_instance(sys.stdin)
    cut_instance.dump(sys.stdout)


if __name__ == "__main__":
    main()
