from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import HttpRequest, Request
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed

from .game.game import TicTacToeGame


class TicTacToeView(TicTacToeGame, APIView):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self._extra_cookies = {}
        self.extra_data = {}

    def post(self, request: HttpRequest):
        self.clear_games()
        return self.create_game()

    def get(self, request):
        self._requests_counter()
        return self.get_game()

    def put(self, request: Request):
        if "cell" in request.data.keys():
            self._requests_counter()
            return self.set_value(request.data["cell"])
        return Response(data={"error": 'set a number if cell in format {"cell": "cell number"}'})

    def _requests_counter(self):
        if self.game:
            requests_count = int(self.cookies["requests_count"])
            if self.request.method == "GET":
                requests_count += 1
            elif self.request.method == "PUT":
                requests_count = 0
            self.cookies = {"requests_count": str(requests_count)}
            self.__set_single_game_mode_or_delete()

    def __set_single_game_mode_or_delete(self):
        if (not self.game.started) and (int(self.cookies["requests_count"]) >= self.max_request_num):
            self.create_game()
            self.cookies = {"single": "true", "player": self.player_prefix % 1}
        else:
            self.delete_if_max_request()
