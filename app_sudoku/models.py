from django.db import models
from django.contrib.auth.models import User


class SudokuStatisticModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="sudoku_stat")
    games_count = models.IntegerField(default=0)
    winn_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Sudoku: games {self.games_count}, winn {self.winn_count}."

