import datetime
from random import choice


class CreateGame:
    empty_square = {"1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": ""}

    def create_game(self):
        game = self.__get_last_game()
        if game.started:
            game = self.model.objects.create(play_square=self.empty_square)
        else:
            game.started = True
        game.save()
        self.__set_base_cookies(game)
        return self.response

    @classmethod
    def __get_last_game(cls):
        game = cls.model.objects.last()
        if not game:
            game = cls.model.objects.create(play_square=cls.empty_square)
            game.save()
        return game

    def __set_base_cookies(self, game):
        """Set base cookies for just created game"""
        self.cookies = {"game": self.game_name, "game_id": str(game.id), "requests_count": "0", "single": "false"}
        if game.started:
            self.cookies = {"player": self.player_prefix % 2}
        else:
            self.cookies = {"player": self.player_prefix % 1}
        return self.response


class UpdateGame:

    def set_value(self, cell):
        """Sets value in play square returns request with game"""
        self.game = cell
        if self.single:
            self.auto_set_for_single_game()
        return self.response

    def get_game(self):
        """Returns request with square"""
        return self.response

    def game_status(self):
        full_square = self.__check_full_square()
        if full_square:
            return "Friendship is winn!"
        winner = self.__check_winner()
        if winner:
            return self.__get_winner_text(winner)
        return None

    def __get_winner_text(self, winner_character):
        if (self.player == 1 and winner_character == "X") \
        or (self.player == 2 and winner_character == "O"):
            return "You are winn."
        else:
            return "You are lose."

    def __check_full_square(self):
        square = self.game.play_square
        if "" in square.values():
            return False
        return True

    def __check_winner(self):
        square = self.game.play_square
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

    def auto_set_for_single_game(self):
        empty_cells = []
        for key, value in self.game.play_square.items():
            if not value:
                empty_cells.append(key)
        if empty_cells:
            cell = choice(empty_cells)
            self.cookies = {"player": self.player_prefix % 2}
            self.game = cell
            self.cookies = {"player": self.player_prefix % 1}



class DeleteGame:

    def delete_if_max_request(self):
        """Delete game is request number grater then max_request_num"""
        requests_count = int(self.cookies["requests_count"])
        if self.game and (requests_count > self.max_request_num):
            self.delete_game()

    def delete_game(self):
        del self.game

    @classmethod
    def clear_games(cls):
        """Deletes all old games"""
        games = cls.model.objects.all()
        for game in games:
            game_exist = datetime.datetime.now(tz=datetime.timezone.utc) - game.created_date
            if game_exist > datetime.timedelta(seconds=cls.game_lifetime):
                game.delete()


__all__ = [CreateGame, UpdateGame, DeleteGame]
