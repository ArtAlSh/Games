from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import HttpRequest, Request
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed

from .game.game import TicTacToeGame


class TicTacToeView(TicTacToeGame, APIView):

    def get(self, request):
        return self.get_game()

    def post(self, request: HttpRequest):
        return self.create_game()

    def put(self, request: Request):
        if "cell" in request.data.keys():
            return self.set_value(request.data["cell"])
        return Response(data={"error": 'set a number if cell in format {"cell": "cell number"}'})
