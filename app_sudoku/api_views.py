from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework.request import Request
from .sudoku import Sudoku
from .models import SudokuStatisticModel


class SudokuGenerateView(APIView):

    def get(self, request: Request, level="easy"):
        sudoku = Sudoku(level=level)
        # print(request.auth, request.user.is_active)
        data = {
            "level": sudoku.level,
            "statistic": False,
            "play_square": sudoku.play_square,
            "full_square": sudoku.full_square,
        }

        if request.user.is_active:
            data["statistic"] = True
            stat = SudokuStatisticModel.objects.get(user=request.user)
            stat.games_count += 1
            stat.save()

        return Response(data=data, status=status.HTTP_200_OK)

    def put(self, request: Request):
        if request.user.is_active:
            stat = SudokuStatisticModel.objects.get(user=request.user)
            if request.data["is_winn"]:
                stat.winn_count += 1
                stat.save()
            if request.data["add_new"]:
                stat.games_count += 1
                stat.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request: Request):
        if request.user.is_active:
            stat = SudokuStatisticModel.objects.get(user=request.user)
            stat.games_count = 0
            stat.winn_count = 0
        return Response(status=status.HTTP_200_OK)
