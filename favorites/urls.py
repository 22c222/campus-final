from django.urls import path
from . import views

urlpatterns = [
    path('toggle/<int:goods_id>/', views.favorite_toggle, name='favorite_toggle'),
    path('my/', views.my_favorites, name='my_favorites'),
]