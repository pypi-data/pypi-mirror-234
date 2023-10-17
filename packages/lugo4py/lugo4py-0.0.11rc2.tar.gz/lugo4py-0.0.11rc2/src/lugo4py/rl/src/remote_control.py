import threading

import grpc

from ...src import lugo
from ...protos.remote_pb2 import (
    PauseResumeRequest, NextTurnRequest, NextOrderRequest,
    BallProperties, PlayerProperties, GameProperties,
    ResumeListeningRequest
)
from ...protos.remote_pb2_grpc import RemoteStub


class RemoteControl:
    def __init__(self):
        self.client = None

    def connect(self, grpc_address: str) -> None:
        channel = grpc.insecure_channel(grpc_address)
        try:
            grpc.channel_ready_future(channel).result(timeout=15)
        except grpc.FutureTimeoutError:
            raise Exception("timed out waiting to connect to the game server")
        self.client = RemoteStub(channel)

    def pause_resume(self):
        req = PauseResumeRequest()
        try:
            return self.client.PauseOrResume(req)
        except Exception:
            raise Exception("[Remote Control] Failed to pause/resume the game")

    def resume_listening(self, waiter: threading.Event):
        req = ResumeListeningRequest()
        try:
            result = self.client.ResumeListeningPhase(req)
            waiter.set()
            return result
        except Exception:
            raise Exception("[Remote Control] Failed to resume listening phase the game")

    def next_turn(self):
        req = NextTurnRequest()
        try:
            return self.client.NextTurn(req)
        except Exception:
            raise Exception("[Remote Control] Failed to play to next turn")

    def next_order(self):
        req = NextOrderRequest()
        try:
            return self.client.NextOrder(req)
        except Exception:
            raise Exception("[Remote Control] Failed to play to next order")

    def set_ball_rops(self, position: lugo.Point, velocity: lugo.Velocity):
        req = BallProperties(position=position, velocity=velocity)
        response = self.client.SetBallProperties(req)
        return response

    def set_player_props(self, team_side: lugo.TeamSide, player_number: int, new_position: lugo.Point,
                         new_velocity: lugo.Velocity):
        req = PlayerProperties(
            side=team_side, number=player_number,
            position=new_position, velocity=new_velocity
        )
        response = self.client.SetPlayerProperties(req)
        return response

    def set_game_props(self, turn: int):
        req = GameProperties(turn=turn)
        response = self.client.SetGameProperties(req)
        return response
