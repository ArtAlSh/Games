from rest_framework import status
from rest_framework.response import Response


class GameCookies:
    """The class separates cookies, checks and returns required cookies"""

    def __get__(self, instance, owner):
        cookies = self._get_cookies(instance, owner)
        cookies.update(instance._extra_cookies)
        if self.check_cookies(cookies, owner):
            return cookies
        return None

    def __set__(self, instance, value: dict):
        for key, val in value.items():
            if key in instance.required_cookies:
                instance._extra_cookies[key] = val

    def __delete__(self, instance):
        instance._extra_cookies = {}

    @staticmethod
    def _get_cookies(instance, owner):
        cookies = {}
        for value in owner.required_cookies:
            cookies[value] = instance.request.COOKIES.get(value)
        return cookies

    @staticmethod
    def check_cookies(cookies, owner):
        if cookies['game'] != owner.game_name: return False
        if not cookies['game_id'].isnumeric(): return False
        if cookies['player'] not in [owner.player_prefix % 1, owner.player_prefix % 2]: return False
        if not cookies['requests_count'].isnumeric(): return False
        if not (cookies['single'] == 'true' or cookies['single'] == 'false'): return False
        return True


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
            try:
                game_id = int(instance.cookies["game_id"])
                game = instance.model.objects.get(id=game_id)
                return game
            except:
                return None
        else:
            return None

    @staticmethod
    def _check_before_set_value(instance, game, cell):
        if not game: return False
        if str(cell) not in game.play_square.keys(): return False
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
        response.data.update(instance.extra_data)
        # check end of game
        game_status = instance.game_status()
        if game_status:
            response.data["winner"] = game_status
            response = self._delete_cookies(response, instance.cookies)
            return response
        response = self._set_cookies(instance, response)
        return response

    @staticmethod
    def _set_cookies(instance, response):
        """Sets (updates) required cookies in request"""
        for key, value in instance.cookies.items():
            response.set_cookie(key=key, value=value,
                                max_age=instance.cookies_max_age,
                                httponly=instance.cookies_httpOnly)
        return response

    @staticmethod
    def _delete_cookies(response, required_cookies):
        for key in required_cookies.keys():
            response.delete_cookie(key=key)
        return response


__all__ = [Game, GameCookies, GameResponse]
