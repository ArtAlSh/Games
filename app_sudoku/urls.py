from django.urls import path
from .api_views import SudokuGenerateView

urlpatterns = [
    path('', SudokuGenerateView.as_view(), name="sudoku"),
    path('<str:level>/', SudokuGenerateView.as_view(), name="sudoku_level"),
]
