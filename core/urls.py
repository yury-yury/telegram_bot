from django.contrib import admin
from django.urls import path, include

from core.views import UserCreateView

urlpatterns = [
    path('signup/', UserCreateView.as_view()),
]
