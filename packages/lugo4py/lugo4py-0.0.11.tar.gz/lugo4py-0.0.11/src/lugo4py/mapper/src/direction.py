from ...protos.physics_pb2 import Point

from ...src.specs import *
from ...src.goal import Goal
from ...protos import server_pb2
from enum import IntEnum

class DIRECTION(IntEnum):
    FORWARD = 0
    BACKWARD = 1,
    LEFT = 2,
    RIGHT = 3,
    BACKWARD_LEFT = 4,
    BACKWARD_RIGHT = 5,
    FORWARD_LEFT = 6,
    FORWARD_RIGHT = 7

DIRECTION_FORWARD = DIRECTION.FORWARD
DIRECTION_BACKWARD = DIRECTION.BACKWARD
DIRECTION_LEFT = DIRECTION.LEFT
DIRECTION_RIGHT = DIRECTION.RIGHT
DIRECTION_BACKWARD_LEFT = DIRECTION.BACKWARD_LEFT
DIRECTION_BACKWARD_RIGHT = DIRECTION.BACKWARD_RIGHT
DIRECTION_FORWARD_LEFT = DIRECTION.FORWARD_LEFT
DIRECTION_FORWARD_RIGHT = DIRECTION.FORWARD_RIGHT

homeGoalCenter = Point()
homeGoalCenter.x = 0
homeGoalCenter.y = int(MAX_Y_COORDINATE / 2)

homeGoalTopPole = Point()
homeGoalTopPole.x = 0
homeGoalTopPole.y = int(GOAL_MAX_Y)

homeGoalBottomPole = Point()
homeGoalBottomPole.x = 0
homeGoalBottomPole.y = int(GOAL_MIN_Y)

awayGoalCenter = Point()
awayGoalCenter.x = int(MAX_X_COORDINATE)
awayGoalCenter.y = int(MAX_Y_COORDINATE / 2)

awayGoalTopPole = Point()
awayGoalTopPole.x = int(MAX_X_COORDINATE)
awayGoalTopPole.y = int(GOAL_MAX_Y)

awayGoalBottomPole = Point()
awayGoalBottomPole.x = int(MAX_X_COORDINATE)
awayGoalBottomPole.y = int(GOAL_MIN_Y)

awayGoal = Goal(
    server_pb2.Team.Side.AWAY,
    awayGoalCenter,
    awayGoalTopPole,
    awayGoalBottomPole
)
homeGoal = Goal(
    server_pb2.Team.Side.HOME,
    homeGoalCenter,
    homeGoalTopPole,
    homeGoalBottomPole
)