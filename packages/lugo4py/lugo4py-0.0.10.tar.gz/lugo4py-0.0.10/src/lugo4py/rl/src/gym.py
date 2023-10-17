import time

from .training_controller import TrainingCrl
from .helper_bots import newChaserHelperPlayer, newZombieHelperPlayer
from .remote_control import RemoteControl
from .interfaces import BotTrainer, TrainingFunction
from ...src import client
from ...protos.server_pb2 import Team
import threading

from concurrent.futures import ThreadPoolExecutor


class Gym:

    def __init__(
            self,
            executor: ThreadPoolExecutor,
            remote_control: RemoteControl,
            trainer: BotTrainer,
            trainingFunction: TrainingFunction,
            options=None,
    ):
        if options is None:
            options = {"debugging_log": False}

        self.remoteControl = remote_control
        self.debugging_log = options["debugging_log"]
        self.trainingCrl = TrainingCrl(executor,
                                       remote_control, trainer, trainingFunction)

        self.trainingCrl.logger = self._debug
        self.gameServerAddress = None
        self.helperPlayers = None
        self.players = []

    def start(self, lugo_client: client.LugoClient, executor: ThreadPoolExecutor):
        hasStarted = False

        def play_callback(orderSet, snapshot):
            nonlocal hasStarted
            hasStarted = True
            return self.trainingCrl.gameTurnHandler(orderSet, snapshot)

        def trigger_listening() -> None:
            nonlocal hasStarted
            if hasStarted is False:
                waiter = threading.Event()
                executor.submit(self.remoteControl.resume_listening, waiter)
                waiter.wait()

        def on_join() -> None:
            self._debug('The main bot is connected!! Starting to connect the zombies')
            time.sleep(0.2)
            if self.gameServerAddress:
                self.players = self.helperPlayers(self.gameServerAddress, executor)
            self._debug('helpers are done')
            trigger_listening()

        lugo_client.play(executor, play_callback, on_join)
        return lugo_client

    def stop(self):
        self.trainingCrl.stop()
        for player in self.players:
            player.stop()

    def with_zombie_players(self, game_server_address):
        self._debug('Entering with_zombie_players\n')
        self.gameServerAddress = game_server_address
        self.helperPlayers = create_helper_players
        return self

    def withChasersPlayers(self, game_server_address):
        self.gameServerAddress = game_server_address

        def helper_players(game_server_address):
            for i in range(1, 12):
                newChaserHelperPlayer(Team.Side.HOME, i, game_server_address)
                newChaserHelperPlayer(Team.Side.AWAY, i, game_server_address)

        self.helperPlayers = helper_players(game_server_address)
        return self

    def _debug(self, message: str):
        if self.debugging_log:
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"[Debugger {t}] {message}")


def create_helper_players(gameServerAddress: str, executor: ThreadPoolExecutor):
    children = []
    for i in range(0, 11):
        time.sleep(0.01)
        children.append(newZombieHelperPlayer(Team.Side.HOME, i + 1, gameServerAddress, executor))
        time.sleep(0.01)
        children.append(newZombieHelperPlayer(Team.Side.AWAY, i + 1, gameServerAddress, executor))
    return children
