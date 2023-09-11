from django.urls import path

from messanger.views import SentMessageView

urlpatterns = [
    path('sent', SentMessageView.as_view()),
    ]
