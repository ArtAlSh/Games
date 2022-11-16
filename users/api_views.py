from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.authentication import authenticate
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.authtoken.models import Token

from .serializers import UserSignUpSerializer
from .models import SudokuStatisticModel


class SignUpView(generics.CreateAPIView):
    serializer_class = UserSignUpSerializer
    permission_classes = [permissions.AllowAny]


class LogInView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request=request, username=username, password=password)
        if user:
            token = Token.objects.get(user=user)
            data = {"username": user.username, "token": token.key}
            return Response(data=data, status=status.HTTP_200_OK)

        data = {"error": "wrong credentials"}
        return Response(data=data, status=status.HTTP_409_CONFLICT)


class UserPageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request):
        sudoku_stat = SudokuStatisticModel.objects.get(user=request.user)
        data = {
            "sudoku": {
                "games_count": sudoku_stat.games_count,
                "winn_count": sudoku_stat.winn_count,
            }
        }
        return Response(data=data, status=status.HTTP_200_OK)
