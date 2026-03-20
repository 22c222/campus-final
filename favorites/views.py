from django.shortcuts import redirect, render
from .models import Favorite
from goods.models import Goods
from users.models import MarketUser


def favorite_toggle(request, goods_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/users/login/')

    goods = Goods.objects.get(id=goods_id)
    user = MarketUser.objects.get(id=user_id)

    favorite = Favorite.objects.filter(user=user, goods=goods).first()

    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(user=user, goods=goods)

    return redirect(f'/goods/detail/{goods_id}/')


def my_favorites(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/users/login/')

    favorite_list = Favorite.objects.filter(user_id=user_id).select_related('goods').order_by('-id')
    username = request.session.get('username', '')

    return render(request, 'my_favorites.html', {
        'favorite_list': favorite_list,
        'username': username
    })