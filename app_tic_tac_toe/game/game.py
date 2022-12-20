from .game_attrs import Game, GameCookies, GameResponse
from .game_base import CreateGame, UpdateGame, DeleteGame

from ..models import TicTacToeGameModel


class TicTacToeGame(CreateGame, UpdateGame, DeleteGame):
    game_name = "tic-tac-toe"
    player_prefix = "player%s"
    model = TicTacToeGameModel

    required_cookies = ("game", "game_id", "player", "requests_count")
    cookies_max_age = 600
    cookies_httpOnly = True

    # game properties:
    cookies = GameCookies()
    game = Game()
    response = GameResponse(required_cookies=required_cookies,
                            max_age=cookies_max_age,
                            httponly=cookies_httpOnly)

    @property
    def your_turn(self) -> bool:
        """
        Checks player's queue.
        If player's turn he can set value in play square.
        """
        return (self.player == 1 and self.game.queue) or \
               (self.player == 2 and not self.game.queue)

    @property
    def player(self):
        """Returns player's number"""
        return int(self.cookies["player"].strip()[-1])

    # in progress
    def _requests_count(self):
        if self.request.method == "GET":
            self.cookies["requests_count"] = str(int(self.cookies["requests_count"]) + 1)
            # delete game if requests more then max_requests_number
        else:
            self.cookies["requests_count"] = "0"
