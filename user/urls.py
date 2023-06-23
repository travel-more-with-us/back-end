from django.urls import path
from user.views import UserSignUpView, UserLoginView

urlpatterns = [
    path('signup/', UserSignUpView, name='signup'),
    path('login/', UserLoginView, name='login'),
]
