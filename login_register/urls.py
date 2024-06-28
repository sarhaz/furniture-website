from django.urls import path
from .views import UserLoginView, UserRegisterView, UserLogoutView

urlpatterns = [
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
    path('accounts/register/', UserRegisterView.as_view(), name='register')
]