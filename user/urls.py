from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from user.views import UserSignUpView, UserLoginView

urlpatterns = [
    path("signup/", UserSignUpView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path(
        "api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
]
