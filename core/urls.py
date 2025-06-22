# imad/core/urls.py

from django.urls import path
from . import views

# This is a special Django variable that helps organize URLs by app name
app_name = 'core'

urlpatterns = [
    # This file should ONLY contain the URL for your public homepage.
    # The empty path '' matches the root URL (e.g., http://127.0.0.1:8000/).
    path('', views.home, name='home'),
]