from django.urls import path
from .views import *

urlpatterns = [
    path('webhook', instagram_webhook, name='instagram_webhook')
]


