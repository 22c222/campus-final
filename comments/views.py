from django.shortcuts import redirect
from .models import Comment
from goods.models import Goods
from users.models import MarketUser


def comment_create(request, goods_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/users/login/')

    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            goods = Goods.objects.get(id=goods_id)
            user = MarketUser.objects.get(id=user_id)

            Comment.objects.create(
                goods=goods,
                user=user,
                content=content
            )

    return redirect(f'/goods/detail/{goods_id}/')