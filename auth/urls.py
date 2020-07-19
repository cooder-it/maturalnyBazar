from django.urls import path
from .views import login_user, register_user

urlpatterns = [
    path('login/', login_user),
    path('register/', register_user),
]