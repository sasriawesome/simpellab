from django.urls import path

from .views import shortener_view

urlpatterns = [
    path('<str:hashed_url>/', shortener_view, name='goto_shorturl')
]