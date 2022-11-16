from django.urls import path
from .api_views import SignUpView, LogInView, UserPageView

urlpatterns = [
    path('sign_up/', SignUpView.as_view(), name="signup"),
    path('log_in/', LogInView.as_view(), name="login"),
    path('statistic/', UserPageView.as_view(), name="statistic"),
]
