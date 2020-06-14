"""Representation of cutting problems."""

from typing import NamedTuple


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

    @property
    def is_open(self) -> bool:
        """Tell if this is an open polyline."""
        return not self.is_closed

    def __str__(self) -> str:
        return "Polyline({}, {} -> {}, {})".format(
            self.name,
            self.start,
            self.end,
            "closed" if self.is_closed else "open",
        )
