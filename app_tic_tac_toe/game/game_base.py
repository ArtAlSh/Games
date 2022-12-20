from rest_framework import status
from rest_framework.response import Response


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
            your_turn = False
        else:
            cookies["player"] = cls.player_prefix % "1"
            your_turn = True

        response = Response(
            data={"play_square": game.play_square, "started": game.started,
                  "your_turn": your_turn, "winner": ""},
            status=status.HTTP_201_CREATED
        )
        # set cookies in response
        for key, value in cookies.items():
            response.set_cookie(key, value, max_age=cls.cookies_max_age, httponly=cls.cookies_httpOnly)
        return response


class UpdateGame:

    def set_value(self, cell):
        """Sets value in play square returns request with game"""
        self.game = cell
        return self.response

    def get_game(self):
        """Returns request with square"""
        return self.response


class DeleteGame:
    pass


__all__ = [CreateGame, UpdateGame, DeleteGame]
