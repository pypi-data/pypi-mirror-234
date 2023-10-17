import asyncio
from .remote_control import RemoteControl
from .interfaces import TrainingController, BotTrainer, TrainingFunction
from ...protos.server_pb2 import GameSnapshot, OrderSet
import threading
from concurrent.futures import ThreadPoolExecutor
import time




class TrainingCrl(TrainingController):

    def __init__(self, executor: ThreadPoolExecutor, remoteControl: RemoteControl, bot: BotTrainer, onReadyCallback: TrainingFunction):
        self._gotNextState = lambda snapshot: print("got first snapshot")
        self.logger = lambda msg: print(f'set debugger')
        self.previousState = None
        self.remoteControl = remoteControl  # type: RemoteControl
        self.onReady = onReadyCallback
        self.trainingHasStarted = False
        self.lastSnapshot = None  # type: GameSnapshot
        self.onListeningMode = False
        self.OrderSet = None
        self.cycleSeq = 0
        self.bot = bot  # type: BotTrainer
        self.debugging_log = False
        self.stopRequested = threading.Event()
        self.trainingExecutor = executor
        self.resumeListeningPhase = lambda action: print(
            'resumeListeningPhase not defined yet - should wait the initialise it on the first "update" call')

    def set_environment(self, data):
        self.logger('Reset state')
        try:
            self.lastSnapshot = self.bot.set_environment(data)
            return self.bot.get_state(self.lastSnapshot)
        except Exception as e:
            print('bot trainer failed to create initial state: ', e)
            raise e

    def get_state(self):
        try:
            self.cycleSeq = self.cycleSeq + 1
            self.logger('get state')
            return self.bot.get_state(self.lastSnapshot)
        except Exception as e:
            print('bot trainer failed to return inputs from a particular state', e)
            raise e

    def update(self, action: any):
        self.logger('received action from training bot')
        if not self.onListeningMode:
            raise ValueError('faulty synchrony - got a new action when was still processing the last one')

        try:
            previousState = self.lastSnapshot
            self.OrderSet.turn = self.lastSnapshot.turn
            updatedOrderSet = self.bot.play(self.OrderSet, self.lastSnapshot, action)

            self.logger('got order set, passing down')

            self.resumeListeningPhase(updatedOrderSet)
            #time.sleep(2.4)  # before calling next turn, let's wait just a bit to ensure the server got our order
            self.lastSnapshot = self.wait_until_next_listening_state()

            self.logger('got new snapshot after order has been sent')

            if self.stopRequested.is_set():
                return None

            # TODO: if I want to skip the net N turns? I should be able too
            self.logger(f"update finished (turn {self.lastSnapshot.turn} waiting for next action)")
        except Exception as e:
            print('failed send new action to the server: ', e)
            raise e

        try:
            return self.bot.evaluate(previousState, self.lastSnapshot)
        except Exception as e:
            print('bot trainer failed to evaluate game state', e)
            raise e

    def gameTurnHandler(self, order_set, snapshot):
        if self.stopRequested.is_set():
            self.logger('skipping turn handler because the stop request')
            return None
        self.logger('new turn')
        if self.onListeningMode:
            raise RuntimeError(
                "faulty synchrony - got new turn while waiting for order (check the lugo 'timer-mode')")

        self._gotNextState(snapshot)
        self.OrderSet = order_set

        waiter = threading.Event()
        new_order_set = None

        def resume(updated_order_set):
            nonlocal new_order_set
            new_order_set = updated_order_set
            waiter.set()
            self.logger(f'Sending new action')

        self.resumeListeningPhase = resume
        self.onListeningMode = True
        if self.trainingHasStarted is False:
            self.trainingExecutor.submit(self.onReady, self, self.stopRequested)
            self.trainingHasStarted = True
            self.logger(f'the training has started')

        self.logger(f'Waiting get new update!')
        waiter.wait(timeout=5)
        self.logger(f'order sent to the game server')
        return new_order_set

    def wait_until_next_listening_state(self) -> GameSnapshot:
        try:
            self.onListeningMode = False
            waiter = threading.Event()

            new_snapshot = None
            def resume(newGameSnapshot):
                nonlocal new_snapshot
                new_snapshot = newGameSnapshot
                waiter.set()

            self._gotNextState = resume


            waiterResumeListening = threading.Event()
            self.trainingExecutor.submit(self.remoteControl.resume_listening, waiterResumeListening)
            waiterResumeListening.wait()

            waiter.wait(timeout=3)
            if new_snapshot is None:
                raise RuntimeError(
                    "timed out waiting for the next listening state - check the training controller")

            self.logger(f'resume_listening: {new_snapshot.turn}')

            return new_snapshot
        except Exception as e:
            self.logger(f'failed to send the orders to the server {e}')
            raise

    def stop(self):
        self.stopRequested.set()


