from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import HttpRequest, Request
from rest_framework.response import Response

from .models import TicTacToeGameModel


class TicTacToeView(APIView):

    def get(self, request: HttpRequest):
        if request.COOKIES.get("game") == "tic-tac-toe":
            game = self.get_game(request.COOKIES.get("game_is"))
            return Response(data=game.play_square, status=status.HTTP_200_OK)

        game = self._create_game()
        response = Response(data=game.play_square, status=status.HTTP_201_CREATED)
        cookies = {"game": "tic-tac-toe", "game_id": str(game.id)}

        if game.started:
            cookies["user"] = "user2"
            cookies["your_turn"] = "false"
        else:
            cookies["user"] = "user1"
            cookies["your_turn"] = "true"
        response = self._set_cookies(response, cookies)
        return response

    def put(self, request: Request):
        """Put data in format {"cell": "5"}"""
        cookies = self._get_cookies(request)
        # add try-except block
        game = self.get_game(cookies["game_id"])

        check_users_queue = (cookies["user"] == "user1" and game.queue) or (cookies["user"] == "user2" and not game.queue)
        check_cell = not bool(game.play_square[request.data["cell"]])
        if game.started and check_users_queue and check_cell:
            cookies["your_turn"] = str(cookies["user"] == "user1" and game.queue).lower()
            play_square = self._set_value_in_square(
                square=game.play_square, cell=request.data["cell"], user=cookies["user"])
            game.play_square = play_square
            game.queue = not game.queue
            game.save()

        response = Response(data=game.play_square, status=status.HTTP_200_OK)
        response = self._set_cookies(response, cookies)
        return response

    def get_game(self, game_id):
        game = TicTacToeGameModel.objects.get(id=game_id)
        return game

    def _set_value_in_square(self, square, cell, user):
        if user == "user1":
            square[cell] = "X"
        elif user == "user2":
            square[cell] = "O"
        return square

    def _create_game(self):
        empty_square = {"1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": ""}
        game = TicTacToeGameModel.objects.last()
        if game.started:
            game = TicTacToeGameModel.objects.create(play_square=empty_square)
        else:
            game.started = True
        game.save()
        return game

    def _get_cookies(self, request: HttpRequest):
        cookies_list = ("game", "game_id", "user", "your_turn")
        cookies = {}
        for value in cookies_list:
            cookies[value] = request.COOKIES.get(value)
        return cookies

    def _set_cookies(self, response: Response, cookies: dict):
        max_age = 600
        httpOnly = True
        for key, value in cookies.items():
            response.set_cookie(key=key, value=value, max_age=max_age, httponly=httpOnly)
        return response
