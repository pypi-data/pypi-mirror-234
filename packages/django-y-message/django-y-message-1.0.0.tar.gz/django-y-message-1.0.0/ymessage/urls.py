from django.urls import path

from . import views

urlpatterns = [
    path('default_message_handler/', views.default_message_handler),
]
