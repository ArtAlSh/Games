from .game_attrs import Game, GameCookies, GameResponse
from .game_base import CreateGame, UpdateGame, DeleteGame

from ..models import TicTacToeGameModel

from rest_framework.response import Response


class TicTacToeGame(CreateGame, UpdateGame, DeleteGame):
    game_name = "tic-tac-toe"
    player_prefix = "player%s"
    model = TicTacToeGameModel

    # cookies parameters
    required_cookies = ("game", "game_id", "player", "requests_count", "single")
    cookies_max_age = 20
    cookies_httpOnly = True

    # game deletion parameters
    max_request_num = 15
    game_lifetime = cookies_max_age * 9

    # game properties:
    cookies = GameCookies()
    game = Game()
    response = GameResponse()

    @property
    def your_turn(self) -> bool:
        """
        Checks player's queue.
        If player's turn he can set value in play square.
        """
        if (not self.player) or (not self.game): return None
        return (self.player == 1 and self.game.queue) or \
               (self.player == 2 and not self.game.queue)

    @property
    def player(self):
        """Returns player's number"""
        if not self.cookies: return None
        return int(self.cookies["player"].strip()[-1])

    @property
    def single(self):
        if not self.cookies: return None
        return self.cookies["single"] == "true"
