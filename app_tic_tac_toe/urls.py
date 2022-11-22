from django.urls import path
from .api_views import TicTacToeView

urlpatterns = [
    path('', TicTacToeView.as_view(), name='tic-tac-toe'),
]
