from ..src import lugo, snapshot
from ..mapper import Mapper
from abc import ABC, abstractmethod


class PlayerState(object):
    """
     Represents various states that a player can be in during a game.

     Attributes:
         SUPPORTING (int): The player does not hold the ball, but the holder is a teammate
         HOLDING_THE_BALL (int): The player is holding the ball.
         DEFENDING (int): The ball holder is an opponent player
         DISPUTING_THE_BALL (int): No one is holding the ball

     Methods:
         None
     """
    SUPPORTING = 0
    HOLDING_THE_BALL = 1
    DEFENDING = 2
    DISPUTING_THE_BALL = 3


PLAYER_STATE = PlayerState()


class Bot(ABC):
    """
    Abstract base class representing a bot in a game.

    Attributes:
        side (TeamSide): The side to which the bot belongs.
        number (int): The player number in its team
        init_position (Point): The initial position of the bot.
        mapper (Mapper): The mapper associated with the bot.

    Methods:
        on_disputing(order_set: OrderSet, game_snapshot: GameSnapshot) -> OrderSet: Method called when the player is on DISPUTING_THE_BALL state
        on_defending(order_set: OrderSet, game_snapshot: GameSnapshot) -> OrderSet: Method called when the player is on DEFENDING state
        on_holding(order_set: OrderSet, game_snapshot: GameSnapshot) -> OrderSet: Method called when the player is on HOLDING_THE_BALL state
        on_supporting(order_set: OrderSet, game_snapshot: GameSnapshot) -> OrderSet: Method called when the player is on SUPPORTING state
        as_goalkeeper(order_set: OrderSet, game_snapshot: GameSnapshot, state: PLAYER_STATE) -> OrderSet: Method is called on every turn, and the player state is passed at the last parameter.
        getting_ready(game_snapshot: GameSnapshot): Abstract method for bot preparation before the game.

    Usage:
    Define a subclass of Bot and implement the abstract methods for specific bot behaviors.
    """
    def __init__(self, side: lugo.TeamSide, number: int, init_position: lugo.Point, my_mapper: Mapper):
        self.number = number
        self.side = side
        self.mapper = my_mapper
        self.initPosition = init_position

    @abstractmethod
    def on_disputing(self, order_set: lugo.OrderSet, game_snapshot: lugo.GameSnapshot) -> lugo.OrderSet:
        """
        Method called when the player is on DISPUTING_THE_BALL state.

        Args:
            order_set (OrderSet): The current set of orders.
            game_snapshot (GameSnapshot): The current game snapshot.

        Returns:
            OrderSet: The updated set of orders.
        """
        pass

    @abstractmethod
    def on_defending(self, order_set: lugo.OrderSet, game_snapshot: lugo.GameSnapshot) -> lugo.OrderSet:
        """
        Method called when the player is on DEFENDING state

        Args:
            order_set (OrderSet): The current set of orders.
            game_snapshot (GameSnapshot): The current game snapshot.

        Returns:
            OrderSet: The updated set of orders.
        """
        pass

    @abstractmethod
    def on_holding(self, order_set: lugo.OrderSet, game_snapshot: lugo.GameSnapshot) -> lugo.OrderSet:
        """
        Method called when the player is on HOLDING_THE_BALL state

        Args:
            order_set (OrderSet): The current set of orders.
            game_snapshot (GameSnapshot): The current game snapshot.

        Returns:
            OrderSet: The updated set of orders.
        """
        pass

    @abstractmethod
    def on_supporting(self, order_set: lugo.OrderSet, game_snapshot: lugo.GameSnapshot) -> lugo.OrderSet:
        """
        Method called when the player is on SUPPORTING state

        Args:
            order_set (OrderSet): The current set of orders.
            game_snapshot (GameSnapshot): The current game snapshot.

        Returns:
            OrderSet: The updated set of orders.
        """
        pass

    @abstractmethod
    def as_goalkeeper(self, order_set: lugo.OrderSet, game_snapshot: lugo.GameSnapshot,
                      state: PLAYER_STATE) -> lugo.OrderSet:
        """
        Method is called on every turn, and the player state is passed at the last parameter.

        Args:
            order_set (OrderSet): The current set of orders.
            game_snapshot (GameSnapshot): The current game snapshot.
            state (PLAYER_STATE): The current state of the bot.

        Returns:
            OrderSet: The updated set of orders.
        """
        pass

    @abstractmethod
    def getting_ready(self, game_snapshot: lugo.GameSnapshot):
        """
        Method called before the game starts and right after the score is changed

        Args:
            game_snapshot (GameSnapshot): The current game snapshot.
        """
        pass

    def make_reader(self, game_snapshot: lugo.GameSnapshot):
        """
        Create a game snapshot reader for the bot's side and retrieve the bot's player information.

        Args:
            game_snapshot (GameSnapshot): The current game snapshot.

        Returns:
            snapshot.GameSnapshotReader: The game snapshot reader for the bot's side.
            Player: The bot's player information.

        Raises:
            AttributeError: If the bot is not found in the game snapshot.
        """
        reader = snapshot.GameSnapshotReader(game_snapshot, self.side)
        me = reader.get_player(self.side, self.number)
        if me is None:
            raise AttributeError("did not find myself in the game")

        return reader, me


def define_state(game_snapshot: lugo.GameSnapshot, player_number: int, side: lugo.TeamSide) -> PLAYER_STATE:
    if not game_snapshot or not game_snapshot.ball:
        raise AttributeError(
            'invalid snapshot state - cannot define player state')

    reader = snapshot.GameSnapshotReader(game_snapshot, side)
    me = reader.get_player(side, player_number)
    if me is None:
        raise AttributeError(
            'could not find the bot in the snapshot - cannot define player state')

    ball_holder = game_snapshot.ball.holder

    if ball_holder.number == 0:
        return PLAYER_STATE.DISPUTING_THE_BALL

    if ball_holder.team_side == side:
        if ball_holder.number == player_number:
            return PLAYER_STATE.HOLDING_THE_BALL

        return PLAYER_STATE.SUPPORTING

    return PLAYER_STATE.DEFENDING
