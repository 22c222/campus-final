from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:goods_id>/', views.comment_create, name='comment_create'),
]