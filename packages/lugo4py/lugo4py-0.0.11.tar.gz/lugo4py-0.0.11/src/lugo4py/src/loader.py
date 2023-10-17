import os

from . import specs

from ..protos import server_pb2


class EnvVarLoader:

    def __init__(self):
        self._grpcUrl = ""
        self._grpcInsecure = True
        self._botTeamSide = None
        self._botNumber = None
        self._botToken = ""

        if "BOT_TEAM" not in os.environ:
            raise SystemError("missing BOT_TEAM env value")

        if "BOT_NUMBER" not in os.environ:
            raise SystemError("missing BOT_NUMBER env value")

        # the Lugo address
        self._grpcUrl = os.environ.get('BOT_GRPC_URL', 'localhost:5000')
        self._grpcInsecure = bool(os.environ.get('BOT_GRPC_INSECURE', 'false'))

        # defining bot side
        self._botTeamSide = server_pb2.Team.Side.HOME if os.environ[
                                                             "BOT_TEAM"].upper() == 'HOME' else server_pb2.Team.Side.AWAY
        self._botNumber = int(os.environ["BOT_NUMBER"])
        if self._botNumber < 1 or self._botNumber > specs.MAX_PLAYERS:
            raise SystemError('invalid bot number {self._botNumber}, must be between 1 and {specs.MAX_PLAYERS}')

        # // the token is mandatory in official matches, but you may ignore in local games
        self._botToken = os.environ["BOT_TOKEN"] if "BOT_TOKEN" in os.environ else ''

    def get_grpc_url(self):
        return self._grpcUrl

    def get_grpc_insecure(self):
        return self._grpcInsecure

    def get_bot_team_side(self):
        return self._botTeamSide

    def get_bot_number(self):
        return self._botNumber

    def get_bot_token(self):
        return self._botToken
