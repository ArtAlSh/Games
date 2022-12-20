from rest_framework import status
from rest_framework.response import Response


class GameCookies:
    """The class separates cookies, checks and returns required cookies"""

    def __get__(self, instance, owner):
        cookies = self._get_cookies(instance, owner)
        if cookies["game"] == owner.game_name:
            return cookies
        else:
            return None

    @staticmethod
    def _get_cookies(instance, owner):
        cookies = {}
        for value in owner.required_cookies:
            cookies[value] = instance.request.COOKIES.get(value)
        return cookies


class Game:
    """
    The class works with game model.
    __get__ return game model.
    __set__ set "O" or "X" in game square. Require number of cell from 1 to 9
    __del__ delete game model
    """

    def __get__(self, instance, owner):
        return self._get_game(instance)

    def __set__(self, instance, value):
        game = self._get_game(instance)
        if self._check_before_set_value(instance, game, value):
            self._set_value(instance, game, value)

    def __delete__(self, instance):
        game = self._get_game(instance)
        if game: game.delete()

    @staticmethod
    def _get_game(instance):
        """Returns game model if exist or None"""
        if instance.cookies:
            game_id = instance.cookies["game_id"]
            return instance.model.objects.get(id=game_id)
        else:
            return None

    @staticmethod
    def _check_before_set_value(instance, game, cell):
        if not game:
            return False
        empty_cell = not game.play_square[str(cell)]
        return game.started and instance.your_turn and empty_cell

    @staticmethod
    def _set_value(instance, game, cell):
        """Set 'O' for player1 or 'X' for player2 in game.play_square."""
        if instance.player == 1:
            game.play_square[str(cell)] = "X"
        elif instance.player == 2:
            game.play_square[str(cell)] = "O"
        else:
            return 0
        game.queue = not game.queue
        game.save()


class GameResponse:

    def __init__(self, required_cookies, max_age, httponly):
        self.required_cookies = required_cookies
        self.cookies_max_age = max_age
        self.cookies_httpOnly = httponly

    def __get__(self, instance, owner):
        if instance.game:
            return self._response(instance)
        return Response(data={"warning": "You didn't start any game."}, status=status.HTTP_204_NO_CONTENT)

    def _response(self, instance):
        # base response
        response = Response(
            data={"play_square": instance.game.play_square, "started": instance.game.started,
                  "your_turn": instance.your_turn, "winner": ""},
            status=status.HTTP_200_OK
        )
        # check end game
        check_winner = self._check_winner(square=instance.game.play_square)
        check_full_square = self._check_full_square(square=instance.game.play_square)
        # set specific data in request
        if check_winner:
            winner = "You are winn." if (instance.player == 1 and check_winner == "X") \
                                        or (instance.player == 2 and check_winner == "O") \
                else "You are lose."
            response.data["winner"] = winner
            response = self._delete_cookies(response, instance.cookies)
        elif check_full_square:
            response.data["winner"] = "Friendship is winn!"
            response = self._delete_cookies(response, instance.cookies)
        else:
            response = self._set_cookies(response, instance.cookies)
        return response

    def _set_cookies(self, response, required_cookies):
        """Sets (updates) required cookies in request"""
        for key, value in required_cookies.items():
            response.set_cookie(key=key, value=value,
                                max_age=self.cookies_max_age,
                                httponly=self.cookies_httpOnly)
        return response

    @staticmethod
    def _delete_cookies(response, required_cookies):
        for key in required_cookies.keys():
            response.delete_cookie(key=key)
        return response

    @staticmethod
    def _check_full_square(square):
        if "" in square.values():
            return False
        return True

    @staticmethod
    def _check_winner(square):
        # check rows
        if square["1"] == square["2"] == square["3"] != "": return square["1"]
        if square["4"] == square["5"] == square["6"] != "": return square["4"]
        if square["7"] == square["8"] == square["9"] != "": return square["7"]
        # check columns
        if square["1"] == square["4"] == square["7"] != "": return square["1"]
        if square["2"] == square["5"] == square["8"] != "": return square["2"]
        if square["3"] == square["6"] == square["9"] != "": return square["3"]
        # check diagonals
        if square["1"] == square["5"] == square["9"] != "": return square["1"]
        if square["3"] == square["5"] == square["7"] != "": return square["3"]
        return False


__all__ = [Game, GameCookies, GameResponse]
