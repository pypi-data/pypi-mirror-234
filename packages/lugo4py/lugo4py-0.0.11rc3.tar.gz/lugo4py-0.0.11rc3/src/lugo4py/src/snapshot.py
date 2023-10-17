from . import lugo, geo, specs
from ..mapper import DIRECTION, ORIENTATION, homeGoal, awayGoal
from .goal import Goal
from ..mapper.src.orientation import NORTH
from ..protos import server_pb2
from ..protos.physics_pb2 import Point


class GameSnapshotReader:
    """
    Utility class for reading game snapshots and making orders for a bot.

    Attributes:
        snapshot (GameSnapshot): The current game snapshot.
        my_side (TeamSide): The side to which the bot belongs.

    Methods:
        get_my_team() -> Team: Get the team to which the bot belongs.
        get_opponent_team() -> Team: Get the opponent team.
        get_team(side) -> Team: Get a specific team.
        is_ball_holder(player: Player) -> bool: Check if a player is currently holding the ball.
        get_opponent_side() -> TeamSide: Get the opponent's side.
        get_my_goal() -> Goal: Get the goal on the bot's side.
        get_ball() -> Ball: Get the current ball information.
        get_opponent_goal() -> Goal: Get the opponent's goal.
        get_player(side: TeamSide, number: int) -> Player: Get a player by side and number.
        make_order_move_max_speed(origin: Point, target: Point) -> Order: Create a move order with maximum speed.
        make_order_move(origin: Point, target: Point, speed: int) -> Order: Create a move order with a specific speed.
        make_order_move_from_vector(direction: Vector, speed: int) -> Order: Create a move order from a direction vector.
        make_order_move_by_direction(direction: DIRECTION) -> Order: Create a move order by specifying a direction.
        make_order_jump(origin: Point, target: Point, speed: int) -> Order: Create a jump order with a specific speed.
        make_order_kick(ball: Ball, target: Point, speed: int) -> Order: Create a kick order with a specific speed.
        make_order_kick_max_speed(ball: Ball, target: Point) -> Order: Create a kick order with maximum speed.
        make_order_catch() -> Order: Create a catch order.

    """
    def __init__(self, snapshot: lugo.GameSnapshot, my_side: lugo.TeamSide):
        self.snapshot = snapshot
        self.my_side = my_side

    def get_my_team(self) -> lugo.Team:
        return self.get_team(self.my_side)

    def get_opponent_team(self) -> lugo.Team:
        return self.get_team(self.get_opponent_side())

    def get_team(self, side) -> lugo.Team:
        if side == server_pb2.Team.Side.HOME:
            return self.snapshot.home_team

        return self.snapshot.away_team

    def is_ball_holder(self, player: lugo.Player) -> bool:
        ball = self.snapshot.ball

        return ball.holder is not None and ball.holder.team_side == player.team_side and ball.holder.number == player.number

    def get_opponent_side(self) -> lugo.TeamSide:
        if self.my_side == server_pb2.Team.Side.HOME:
            return server_pb2.Team.Side.AWAY

        return server_pb2.Team.Side.HOME

    def get_my_goal(self) -> Goal:
        if self.my_side == server_pb2.Team.Side.HOME:
            return homeGoal

        return awayGoal

    def get_ball(self) -> lugo.Ball:
        return self.snapshot.ball

    def get_opponent_goal(self) -> Goal:
        if self.my_side == server_pb2.Team.Side.HOME:
            return awayGoal

        return homeGoal

    def get_player(self, side: server_pb2.Team.Side, number: int) -> lugo.Player:
        team = self.get_team(side)
        if team is None:
            return None

        for player in team.players:
            if player.number == number:
                return player
        return None

    def make_order_move_max_speed(self, origin: lugo.Point, target: lugo.Point) -> lugo.Order:
        return self.make_order_move(origin, target, specs.PLAYER_MAX_SPEED)

    def make_order_move(self, origin: lugo.Point, target: lugo.Point, speed: int) -> lugo.Order:
        if origin.x == target.x and origin.y == target.y:
            # a vector cannot have zeroed direction. In this case, the player will just be stopped
            return self.make_order_move_from_vector(NORTH, 0)

        direction = geo.new_vector(origin, target)
        direction = geo.normalize(direction)
        return self.make_order_move_from_vector(direction, speed)

    def make_order_move_from_vector(self, direction: lugo.Vector, speed: int) -> lugo.Order:
        order = server_pb2.Order()

        order.move.velocity.direction.CopyFrom(direction)
        order.move.velocity.speed = speed
        return order

    def make_order_move_by_direction(self, direction: DIRECTION) -> lugo.Order:
        if direction == DIRECTION.FORWARD:
            direction_target = ORIENTATION.EAST
            if self.my_side == server_pb2.Team.Side.AWAY:
                direction_target = ORIENTATION.WEST

        elif direction == DIRECTION.BACKWARD:
            direction_target = ORIENTATION.WEST
            if self.my_side == server_pb2.Team.Side.AWAY:
                direction_target = ORIENTATION.EAST

        elif direction == DIRECTION.LEFT:
            direction_target = ORIENTATION.NORTH
            if self.my_side == server_pb2.Team.Side.AWAY:
                direction_target = ORIENTATION.SOUTH

        elif direction == DIRECTION.RIGHT:
            direction_target = ORIENTATION.SOUTH
            if self.my_side == server_pb2.Team.Side.AWAY:
                direction_target = ORIENTATION.NORTH

        elif direction == DIRECTION.BACKWARD_LEFT:
            direction_target = ORIENTATION.NORTH_WEST
            if self.my_side == server_pb2.Team.Side.AWAY:
                direction_target = ORIENTATION.SOUTH_EAST

        elif direction == DIRECTION.BACKWARD_RIGHT:
            direction_target = ORIENTATION.SOUTH_WEST
            if self.my_side == server_pb2.Team.Side.AWAY:
                direction_target = ORIENTATION.NORTH_EAST

        elif direction == DIRECTION.FORWARD_LEFT:
            direction_target = ORIENTATION.NORTH_EAST
            if self.my_side == server_pb2.Team.Side.AWAY:
                direction_target = ORIENTATION.SOUTH_WEST

        elif direction == DIRECTION.FORWARD_RIGHT:
            direction_target = ORIENTATION.SOUTH_EAST
            if self.my_side == server_pb2.Team.Side.AWAY:
                direction_target = ORIENTATION.NORTH_WEST

        else:
            raise AttributeError('unknown direction {direction}')

        return self.make_order_move_from_vector(direction_target, specs.PLAYER_MAX_SPEED)

    def make_order_jump(self, origin: lugo.Point, target: lugo.Point, speed: int) -> lugo.Order:
        direction = ORIENTATION.EAST
        if origin.x != target.x or origin.y != target.y:
            # a vector cannot have zeroed direction. In this case, the player will just be stopped
            direction = geo.new_vector(origin, target)
            direction = geo.normalize(direction)

        new_velocity = lugo.new_velocity(direction)
        new_velocity.speed = speed

        order = server_pb2.Order()
        jump = order.jump
        jump.velocity.CopyFrom(new_velocity)

        return order

    def make_order_kick(self, ball: lugo.Ball, target: Point, speed: int) -> lugo.Order:
        ball_expected_direction = geo.new_vector(ball.position, target)

        # the ball velocity is summed to the kick velocity, so we have to consider the current ball direction
        diff_vector = geo.sub_vector(
            ball_expected_direction, ball.velocity.direction)

        new_velocity = lugo.new_velocity(geo.normalize(diff_vector))
        new_velocity.speed = speed

        order = server_pb2.Order()
        order.kick.velocity.CopyFrom(new_velocity)

        return order

    def make_order_kick_max_speed(self, ball: lugo.Ball, target: Point) -> lugo.Order:
        return self.make_order_kick(ball, target, specs.BALL_MAX_SPEED)

    def make_order_catch(self) -> server_pb2.Order:
        order = server_pb2.Order()
        order.catch.SetInParent()
        return order






