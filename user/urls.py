from django.urls import path
from rest_framework_simplejwt import views as jwt_views


from user.views import UserSignUpView, UserLoginView, ManageUserView

app_name = "user"

urlpatterns = [
    path("signup/", UserSignUpView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path(
        "token/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),
    path(
        "token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh"
    ),
    path("me/", ManageUserView.as_view(), name="manage"),
]
