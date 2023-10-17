"""
File: lugo.py
Author: Angelo Katipunan
Date: May 20, 2023
Description: This file mocks the gRPC methods to help IDEs intellisense.

Python gRPC files are not friendly to IDEs, what makes the intellisense experience very poor or, sometimes, impossible.

In order to help the programmer experience while developing bots, this file mocks the gRPC methods in a more friendly way.

In short, this file content is not used at all by the package, but will guide the IDE to help the devs.
If you are looking for the real implementation of these methods, please look at the `protos` directory (good luck on that)

"""

from enum import IntEnum
from typing import List

from ..protos import physics_pb2


class Vector:
    """
    Represents a two-dimensional vector in a game.

    Attributes:
        x (float): The x-component of the vector.
        y (float): The y-component of the vector.

    Methods:
        None

    Usage:
    vector = Vector(x, y)
    """
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class Point:
    """
    Represents a point with two-dimensional coordinates in a game.

    Attributes:
        x (int): The x-coordinate of the point.
        y (int): The y-coordinate of the point.

    Methods:
        None

    Usage:
    point = Point(x, y)
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Velocity:
    """
    Represents the velocity of an object in a game.

    Attributes:
        direction (Vector): The direction of the velocity.
        speed (float): The speed or magnitude of the velocity.

    Methods:
        None

    """
    def __init__(self, direction=None, speed=0.0):
        self.direction = direction if direction is not None else Vector()
        self.speed = speed


def new_velocity(vector: Vector) -> Velocity:
    """
    Create a new Velocity object based on a Vector.

    This function takes a Vector object and creates a new Velocity object by setting its direction
    components based on the x and y components from the provided Vector.

    Args:
        vector (Vector): A Vector object representing the direction components.

    Returns:
        Velocity: A new Velocity object with the direction components set from the Vector.

    Example:
    vector = Vector(1.0, 0.0)
    velocity = new_velocity(vector)
    """
    v = physics_pb2.Velocity()
    v.direction.x = vector.x
    v.direction.y = vector.y
    return v


# Classes from remote.proto

class RemoteServicer(object):

    def PauseOrResume(self, request, context):
        # TODO: Implement the PauseOrResume method.
        response = CommandResponse()
        return response

    def NextTurn(self, request, context):
        # TODO: Implement the NextTurn method.
        response = CommandResponse()
        return response

    def NextOrder(self, request, context):
        # TODO: Implement the NextOrder method.
        response = CommandResponse()
        return response

    def SetBallProperties(self, request, context):
        # TODO: Implement the SetBallProperties method.
        response = CommandResponse()
        return response

    def SetPlayerProperties(self, request, context):
        # TODO: Implement the SetPlayerProperties method.
        response = CommandResponse()
        return response

    def SetGameProperties(self, request, context):
        # TODO: Implement the SetGameProperties method.
        response = CommandResponse()
        return response

    def ResumeListeningPhase(self, request, context):
        # TODO: Implement the ResumeListeningPhase method.
        response = ResumeListeningResponse()
        return response


class PauseResumeRequest(object):
    def __init__(self):
        pass


class NextTurnRequest(object):
    def __init__(self):
        pass


class NextOrderRequest(object):
    def __init__(self):
        pass


class BallProperties:
    """
    Represents the properties and state of a ball in a game.

    Attributes:
        position (Point): The current position of the ball.
        velocity (Velocity): The velocity of the ball.
        holder: The current holder of the ball (if any).

    Methods:
        None

    """
    def __init__(self, position=None, velocity=None, holder=None):
        self.position = position if position is not None else Point()
        self.velocity = velocity if velocity is not None else Velocity()
        self.holder = holder


class PlayerProperties:
    """
    Represents the properties and state of a player in a game.

    Attributes:
        side: The side to which the player belongs.
        number (int): The player's unique number per team.
        position (Point): The current position of the player.
        velocity (Velocity): The player's velocity.

    Methods:
        None

    """
    def __init__(self, side=None, number=0, position=None, velocity=None):
        self.side = side
        self.number = number
        self.position = position if position is not None else Point()
        self.velocity = velocity if velocity is not None else Velocity()


class GameProperties:
    def __init__(self, turn=0, home_score=0, away_score=0, frame_interval=0, shot_clock=None):
        self.turn = turn
        self.home_score = home_score
        self.away_score = away_score
        self.frame_interval = frame_interval
        self.shot_clock = shot_clock


class CommandResponse:
    class StatusCode(IntEnum):
        SUCCESS = 0
        INVALID_VALUE = 1
        DEADLINE_EXCEEDED = 2
        OTHER = 99

    def __init__(self, code=None, game_snapshot=None, details=''):
        self.code = code if code is not None else CommandResponse.StatusCode.SUCCESS
        self.game_snapshot = game_snapshot
        self.details = details


class ResumeListeningRequest(object):
    def __init__(self):
        pass


class ResumeListeningResponse(object):
    def __init__(self):
        pass


# from file src/server.proto


class TeamSide(IntEnum):
    HOME = 0
    AWAY = 1


class State(IntEnum):
    """
    Represents what state the game is.
    The bots will play when the game is on the LISTENING state

    WAITING		The game is waiting for all players be connected. There is a configurable time limit to wait for players. After this limit expires, the match is considered over.
    GET_READY	The game resets the players position to start the match or to restart the match after a goal.
    LISTENING	The game is waiting for players orders. There is a configurable time window for this phase. After the time limit expires, the server will ignore the missing orders and process the ones it got. (when running on dev mode, the server may allow different behaviours)
    PLAYING	    The game is executing the players' orders in the same sequence they were gotten. If the ball is NOT been holden, its velocity will be processed first. Otherwise, it position will be updated when the ball holder movement be processed. If there is no movement orders from a player, but it has speed greater than 0, it will be processed after all its orders are processed. Each player orders will be processed in the same sequence they were included in the message (e.g. first move, than kick) The ball kick is processed immediately after the order (the ball position is updated as its new velocity after the kick)
    SHIFTING	The game interrupt the match to shift the ball possession. It happens only when the shot time is over (see shot_clock property). The ball will be given to the goalkeeper of the defense team, and the next state will "listening", so the bots will not have time to rearrange before the next turn.
    OVER		The game may be over after any phase. It can be over after Waiting if there is no players connected after the time limit for connections It can be over after GetReady or Listening if there is no enough players (e.g. connection lost) And it also can be over after Playing state if that was the last turn of the match.
    """
    WAITING = 0
    GET_READY = 1
    LISTENING = 2
    PLAYING = 3
    SHIFTING = 4
    OVER = 99


class StatusCode(IntEnum):
    SUCCESS = 0
    UNKNOWN_PLAYER = 1
    NOT_LISTENING = 2
    WRONG_TURN = 3
    OTHER = 99


class Player:
    """
    Represents a player in a game, including their properties and state.

    Attributes:
        number (int): The player's unique number per team.
        position (Point): The current position of the player.
        velocity (Velocity): The player's velocity.
        team_side (TeamSide): The side to which the player belongs.
        init_position (Point): The initial position of the player.

    Methods:
        None

    """
    def __init__(self, number: int, position: Point, velocity: Velocity, team_side: TeamSide, init_position: Point):
        self.number = number

        if position.x is None:
            position.x = 0
        if position.y is None:
            position.y = 0

        self.position = position
        self.velocity = velocity
        self.team_side = team_side
        self.init_position = init_position


class Team:
    """
    Represents a team in a game, including its players, score, and side.

    Attributes:
        players (List[Player]): A list of Player objects representing the team's players.
        score (int): The team's current score.
        side (TeamSide): The side to which the team belongs.

    Methods:
        None

    """
    def __init__(self, players: List[Player], name: str, score: int, side: TeamSide):
        self.players = players
        self.name = name
        self.score = score
        self.side = side


class Ball:
    """
    Represents a ball in a game, including its position, velocity, and the player currently holding it.

    Attributes:
        position (Point): The current position of the ball.
        velocity (Velocity): The velocity of the ball.
        holder (Player): The player currently holding the ball.

    Methods:
        None
    """
    def __init__(self, position: Point, velocity: Velocity, holder: Player):
        self.position = position
        self.velocity = velocity
        self.holder = holder


class ShotClock:
    """
    Represents a shot clock in a game, indicating the remaining turns for a specific team.

    Attributes:
        team_side (TeamSide): The side of the team associated with this shot clock.
        remaining_turns (int): The number of remaining turns for the shot clock.

    Methods:
        None

    Usage:
    shot_clock = ShotClock(team_side, remaining_turns)
    """
    def __init__(self, team_side: TeamSide, remaining_turns: int):
        self.team_side = team_side
        self.remaining_turns = remaining_turns


class JoinRequest:
    def __init__(self, token: str, protocol_version: str, team_side: TeamSide, number: int, init_position: Point):
        self.token = token
        self.protocol_version = protocol_version
        self.team_side = team_side
        self.number = number
        self.init_position = init_position


class GameSnapshot:
    """
    Represents a snapshot of a game's current state at a specific moment.
    Brings all elements on the field: players and ball, and their speed, direction and position
    Brings the teams' scores, game turn, and shot clock

    Attributes:
        state (State): The current state of the game.
        turn (int): The current turn or game phase.
        home_team (Team): The team representing the home side.
        away_team (Team): The team representing the away side.
        ball (Ball): The ball element.
        turns_ball_in_goal_zone (int): The number of turns the ball has spent in the goal zone.
        shot_clock (ShotClock): The game's shot clock, which limits the time a team has possession of the ball.

    Methods:
        None
    """
    def __init__(self, state: State, turn: int, home_team: Team, away_team: Team, ball: Ball,
                 turns_ball_in_goal_zone: int, shot_clock: ShotClock):
        self.state = state
        self.turn = turn
        self.home_team = home_team
        self.away_team = away_team
        self.ball = ball
        self.turns_ball_in_goal_zone = turns_ball_in_goal_zone
        self.shot_clock = shot_clock


class Order:
    """
    Represents a player order to the game server during the listening

    """
    pass


class Move(Order):
    """
    Represents a move order, which includes a specific velocity for an object.

    Attributes:
        velocity (Velocity): The velocity associated with the move order.

    Methods:
        None
    """
    def __init__(self, velocity: Velocity):
        self.velocity = velocity



class Catch(Order):
    pass


class Kick(Order):
    def __init__(self, velocity: Velocity):
        self.velocity = velocity


class Jump(Order):
    def __init__(self, velocity: Velocity):
        self.velocity = velocity


class OrderSet:
    """
    Represents a set of orders for a specific game turn, including a turn number, a list of orders, and a debug message.

    Attributes:
        turn (int): The game turn number associated with this set of orders.
        orders (List[Order]): A list of Order objects representing the orders for this turn.
        debug_message (str): A debug message or information related to the order set.

    Methods:
        None

    """
    def __init__(self, turn: int, orders: List[Order], debug_message: str):
        self.turn = turn
        self.orders = orders
        self.debug_message = debug_message


class OrderResponse:
    def __init__(self, code: StatusCode, details: str):
        self.code = code
        self.details = details
