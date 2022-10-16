from rest_framework.views import APIView, Response
from rest_framework import status
from .serializers import SudokuSerializer
from .sudoku import Sudoku


class SudokuGenerateView(APIView):

    def get(self, request, level="easy"):
        sudoku = Sudoku(level=level)
        data = {
            "level": sudoku.level,
            "play_square": sudoku.play_square,
            "full_square": sudoku.full_square,
        }

        serializer = SudokuSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
