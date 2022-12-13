from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import HttpRequest, Request
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed

from .models import TicTacToeGameModel


class CreateGame:
    @classmethod
    def create_game(cls):
        empty_square = {"1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": ""}
        game = cls.model.objects.last()
        if game.started:
            game = cls.model.objects.create(play_square=empty_square)
        else:
            game.started = True
        game.save()
        response = cls._base_response(game)
        return response

    @classmethod
    def _base_response(cls, game):
        """Creates and returns response with cookies for just created game"""
        cookies = {"game": cls.game_name, "game_id": str(game.id), "requests_count": "0"}
        if game.started:
            cookies["player"] = cls.player_prefix % "2"
            cookies["your_turn"] = False
        else:
            cookies["player"] = cls.player_prefix % "1"
            cookies["your_turn"] = True

        response = Response(
            data={"play_square": game.play_square, "started": game.started,
                  "your_turn": cookies["your_turn"], "winner": ""},
            status=status.HTTP_201_CREATED
        )
        # set cookies in response
        for key, value in cookies.items():
            response.set_cookie(key, value, max_age=cls.cookies_max_age, httponly=cls.cookies_httpOnly)
        return response


class UpdateGame:

    def set_value(self, cell):
        if self._check_before_set_val_in_square(cell):
            self._set_value_in_square(cell)
            return self._response()
        return Response(data={"error": "You can't set value."}, status=status.HTTP_204_NO_CONTENT)

    def get_game(self):
        if hasattr(self, "game"):
            self.cookies["your_turn"] = str(self._get_queue()).lower()
            return self._response()
        return Response(data={"warning": "You didn't start any game."}, status=status.HTTP_204_NO_CONTENT)

    def _check_before_set_val_in_square(self, cell):
        if not hasattr(self, "game"):
            return False
        empty_cell = not self.game.play_square[str(cell)]
        return self.game.started and self.your_turn and empty_cell

    def _set_value_in_square(self, cell):
        if self.player == 1:
            self.game.play_square[cell] = "X"
        elif self.player == 2:
            self.game.play_square[cell] = "O"
        else:
            return 0
        self.game.queue = not self.game.queue
        self.game.save()
        self.cookies["your_turn"] = str(self._get_queue()).lower()

    def _get_queue(self):
        your_turn = (self.player == 1 and self.game.queue) or \
                    (self.player == 2 and not self.game.queue)
        return your_turn

    def _get_cookies(self):
        cookies = {}
        for value in self.required_cookies:
            cookies[value] = self.request.COOKIES.get(value)
        return cookies

    def _delete_cookies(self, response):
        some = {}
        some.keys()
        for key in self.cookies.keys():
            response.delete_cookie(key=key)
        return response

    def _set_cookies(self, response):
        for key, value in self.cookies.items():
            response.set_cookie(key=key, value=value,
                                max_age=self.cookies_max_age, httponly=self.cookies_httpOnly, samesite="None")
        return response

    def _response(self):
        check_winner = self._check_winner()
        response = Response(
                data={"play_square": self.game.play_square, "started": self.game.started, "your_turn": self._get_queue(), "winner": ""},
                status=status.HTTP_200_OK
        )
        if check_winner:
            winner = "You are winn." if (self.player == 1 and check_winner == "X") \
                                       or (self.player == 2 and check_winner == "O") \
                else "You are lose."
            response.data["winner"] = winner
            response = self._delete_cookies(response)
        elif self._check_full_square():
            response.data["winner"] = "Friendship is winn!"
            response = self._delete_cookies(response)
        else:
            response = self._set_cookies(response)
        return response

    def _check_full_square(self):
        if "" in self.game.play_square.values():
            return False
        return True

    def _check_winner(self):
        square = self.game.play_square
        row1 = square["1"] if square["1"] == square["2"] == square["3"] != "" else False
        row2 = square["4"] if square["4"] == square["5"] == square["6"] != "" else False
        row3 = square["7"] if square["7"] == square["8"] == square["9"] != "" else False

        col1 = square["1"] if square["1"] == square["4"] == square["7"] != "" else False
        col2 = square["2"] if square["2"] == square["5"] == square["8"] != "" else False
        col3 = square["3"] if square["3"] == square["6"] == square["9"] != "" else False

        diag1 = square["1"] if square["1"] == square["5"] == square["9"] != "" else False
        diag2 = square["3"] if square["3"] == square["5"] == square["7"] != "" else False

        check_list = [row1, row2, row3, col1, col2, col3, diag1, diag2]
        for check in check_list:
            if check:
                self.game.finished = True
                self.game.save()
                return check
        return False


class DeleteGame:
    pass


class TicTacToeGame(CreateGame, UpdateGame, DeleteGame):
    game_name = "tic-tac-toe"
    player_prefix = "player%s"
    model = TicTacToeGameModel
    required_cookies = ("game", "game_id", "player", "your_turn", "requests_count")
    cookies_max_age = 600
    cookies_httpOnly = True

    def init_game(self):
        self.cookies = self._get_cookies()
        if self.cookies["game"] == self.game_name and self.request.method in ("GET", "PUT", "DELETE"):
            self.game = self.model.objects.get(id=self.cookies["game_id"])
            self.player = int(self.cookies["player"].strip()[-1])
            self.your_turn = self._get_queue()
            self._requests_count()

    def _requests_count(self):
        if self.request.method == "GET":
            self.cookies["requests_count"] = str(int(self.cookies["requests_count"]) + 1)
            # delete game if requests more then max_requests_number
        else:
            self.cookies["requests_count"] = "0"


class TicTacToeView(TicTacToeGame, APIView):

    def setup(self, request: HttpRequest, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.init_game()

    def get(self, request):
        return self.get_game()

    def post(self, request: HttpRequest):
        return self.create_game()

    def put(self, request: Request):
        if "cell" in request.data.keys():
            return self.set_value(request.data["cell"])
        return Response(data={"error": 'set a number if cell in format {"cell": "cell number"}'})

    def delete(self, request: Request):
        self.delete_game()
        return Response(status=status.HTTP_205_RESET_CONTENT)
