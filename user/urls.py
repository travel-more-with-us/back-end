from django.urls import path
from user.views import UserSignUpView, UserLoginView

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
]
