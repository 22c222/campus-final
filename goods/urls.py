from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.goods_list, name='goods_list'),
    path('api/list/', views.goods_api_list, name='goods_api_list'),
    path('create/', views.goods_create, name='goods_create'),
    path('detail/<int:goods_id>/', views.goods_detail, name='goods_detail'),
    path('delete/<int:goods_id>/', views.goods_delete, name='goods_delete'),
    path('update/<int:goods_id>/', views.goods_update, name='goods_update'),
    path('my/', views.my_goods, name='my_goods'),
]