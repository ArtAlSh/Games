from django.db import models


class TicTacToeGameModel(models.Model):
    """
    User creates game or joins to the last created game.
    If user create game he get a "user1" identificator, else "user2" and set user2=True
    If queue=True user1 can set "X" in play_square. If queue=False user2 can set "O" in play_square.
    play_square is {"1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": ""}
    """
    created_date = models.DateTimeField(auto_now_add=True)
    started = models.BooleanField(default=False)
    queue = models.BooleanField(default=True)
    play_square = models.JSONField()

    def __str__(self):
        square = ""
        for key, value in self.play_square.items():
            square += f"{key}: \"{value}\", "
        square = square[:-2]
        return square
