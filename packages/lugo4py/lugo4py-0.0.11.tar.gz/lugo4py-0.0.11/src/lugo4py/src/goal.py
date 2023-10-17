from . import lugo
from ..protos.physics_pb2 import Point
from ..protos.server_pb2 import Team


class Goal(object):
    """
    Represents a goal element in the field a game.

    Attributes:
        _center (lugo.Point): The center point of the goal.
        _place (lugo.TeamSide): The side to which the goal belongs.
        _topPole (lugo.Point): The top pole of the goal.
        _bottomPole (lugo.Point): The bottom pole of the goal.

    Methods:
        get_center() -> Point: Get the center point of the goal.
        get_place() -> Team.Side: Get the side to which the goal belongs.
        get_top_pole() -> Point: Get the top pole point of the goal.
        get_bottom_pole() -> Point: Get the bottom pole point of the goal.

    Usage:
    goal = Goal(place, center, top_pole, bottom_pole)
    center_point = goal.get_center()
    goal_side = goal.get_place()
    top_pole_point = goal.get_top_pole()
    bottom_pole_point = goal.get_bottom_pole()
    """
    def __init__(self, place: lugo.TeamSide, center: lugo.Point, top_pole: lugo.Point, bottom_pole: lugo.Point):
        self._center = center
        self._place = place
        self._topPole = top_pole
        self._bottomPole = bottom_pole

    def get_center(self) -> Point:
        """
        Get the center point of the goal.

        Returns:
            Point: The center point of the goal.
        """
        return self._center

    def get_place(self) -> Team.Side:
        """
        Get the side to which the goal belongs.

        Returns:
            Team.Side: The side of the team to which the goal belongs.
        """
        return self._place

    def get_top_pole(self) -> Point:
        """
        Get the top pole point of the goal.

        Returns:
            Point: The top pole point of the goal.
        """
        return self._topPole

    def get_bottom_pole(self) -> Point:
        """
        Get the bottom pole point of the goal.

        Returns:
            Point: The bottom pole point of the goal.
        """
        return self._bottomPole
