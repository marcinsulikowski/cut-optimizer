"""Representation of cutting problems."""

from typing import NamedTuple, Sequence, TextIO


class Point(NamedTuple):
    """Point on a 2D plane."""

    x: int  # pylint: disable=invalid-name
    y: int  # pylint: disable=invalid-name

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class Polyline(NamedTuple):
    """Open or closed polyline.

    In case of open polylines, `start` and `end` rare their first and last
    point. In case of closed polylines, they should be corners of of the
    polyline's bounding box.
    """

    name: str
    start: Point
    end: Point
    is_closed: bool

    def __str__(self) -> str:
        return "Polyline({}, {} -> {}, {})".format(
            self.name,
            self.start,
            self.end,
            "closed" if self.is_closed else "open",
        )


class CutInstance:
    """Instance of the curring problem."""

    def __init__(self, polylines: Sequence[Polyline]):
        self.polylines = polylines

    def dump(self, file: TextIO) -> None:
        """Print the instance to the given file."""
        for line in self.polylines:
            print(line, file=file)
