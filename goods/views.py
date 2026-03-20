from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Goods, Category
from users.models import MarketUser
from comments.models import Comment
from favorites.models import Favorite


MAX_PRICE = Decimal("99999999.99")


def validate_price(price_text):
    if not price_text:
        return False, "价格不能为空", None

    try:
        price = Decimal(price_text)
    except (InvalidOperation, ValueError):
        return False, "价格格式不正确，请输入数字", None

    if price < 0:
        return False, "价格不能小于 0", None

    if price > MAX_PRICE:
        return False, f"价格不能超过 {MAX_PRICE}", None

    return True, "", price


def goods_list(request):
    categories = Category.objects.all()
    username = request.session.get('username', '')

    return render(request, 'goods_list.html', {
        'categories': categories,
        'username': username
    })


def goods_api_list(request):
    keyword = request.GET.get('keyword', '').strip()
    category_id = request.GET.get('category', '').strip()

    goods_queryset = Goods.objects.select_related('category', 'user').order_by('-id')

    if keyword:
        goods_queryset = goods_queryset.filter(title__icontains=keyword)

    if category_id and category_id != 'all':
        goods_queryset = goods_queryset.filter(category_id=category_id)

    data = []
    for goods in goods_queryset:
        data.append({
            'id': goods.id,
            'title': goods.title,
            'description': goods.description,
            'price': str(goods.price),
            'contact': goods.contact,
            'category_id': goods.category.id if goods.category else '',
            'category_name': goods.category.name if goods.category else '未分类',
            'seller': goods.user.username if goods.user else '未知用户',
            'created_at': goods.created_at.strftime('%Y-%m-%d %H:%M'),
            'image': goods.image.url if goods.image else '',
        })

    return JsonResponse({
        'code': 200,
        'data': data,
        'msg': '获取成功'
    })


def goods_create(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/users/login/')

    categories = Category.objects.all()
    username = request.session.get('username', '')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        price_text = request.POST.get('price', '').strip()
        contact = request.POST.get('contact', '').strip()
        category_id = request.POST.get('category', '').strip()
        image = request.FILES.get('image')

        if not title or not description or not contact or not category_id:
            return render(request, 'goods_create.html', {
                'categories': categories,
                'username': username,
                'message': '请把表单填写完整',
                'form_data': {
                    'title': title,
                    'description': description,
                    'price': price_text,
                    'contact': contact,
                    'category': category_id,
                }
            })

        ok, error_message, valid_price = validate_price(price_text)
        if not ok:
            return render(request, 'goods_create.html', {
                'categories': categories,
                'username': username,
                'message': error_message,
                'form_data': {
                    'title': title,
                    'description': description,
                    'price': price_text,
                    'contact': contact,
                    'category': category_id,
                }
            })

        user = get_object_or_404(MarketUser, id=user_id)
        category = get_object_or_404(Category, id=category_id)

        Goods.objects.create(
            title=title,
            description=description,
            price=valid_price,
            contact=contact,
            user=user,
            category=category,
            image=image
        )
        return redirect('/goods/list/')

    return render(request, 'goods_create.html', {
        'categories': categories,
        'username': username
    })


def goods_detail(request, goods_id):
    goods = get_object_or_404(Goods, id=goods_id)
    username = request.session.get('username', '')
    user_id = request.session.get('user_id')
    comments = Comment.objects.filter(goods_id=goods_id).select_related('user').order_by('-id')

    is_favorited = False
    if user_id:
        is_favorited = Favorite.objects.filter(user_id=user_id, goods_id=goods_id).exists()

    return render(request, 'goods_detail.html', {
        'goods': goods,
        'username': username,
        'user_id': user_id,
        'comments': comments,
        'is_favorited': is_favorited,
    })


def goods_delete(request, goods_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/users/login/')

    goods = get_object_or_404(Goods, id=goods_id)

    if goods.user_id != user_id:
        return redirect('/goods/list/')

    goods.delete()
    return redirect('/goods/list/')


def goods_update(request, goods_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/users/login/')

    goods = get_object_or_404(Goods, id=goods_id)

    if goods.user_id != user_id:
        return redirect('/goods/list/')

    categories = Category.objects.all()
    username = request.session.get('username', '')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        price_text = request.POST.get('price', '').strip()
        contact = request.POST.get('contact', '').strip()
        category_id = request.POST.get('category', '').strip()
        image = request.FILES.get('image')

        if not title or not description or not contact or not category_id:
            return render(request, 'goods_update.html', {
                'goods': goods,
                'categories': categories,
                'username': username,
                'message': '请把表单填写完整',
            })

        ok, error_message, valid_price = validate_price(price_text)
        if not ok:
            return render(request, 'goods_update.html', {
                'goods': goods,
                'categories': categories,
                'username': username,
                'message': error_message,
            })

        goods.title = title
        goods.description = description
        goods.price = valid_price
        goods.contact = contact
        goods.category = get_object_or_404(Category, id=category_id)

        if image:
            goods.image = image

        goods.save()
        return redirect(f'/goods/detail/{goods.id}/')

    return render(request, 'goods_update.html', {
        'goods': goods,
        'categories': categories,
        'username': username
    })


def my_goods(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/users/login/')

    goods_list = Goods.objects.filter(user_id=user_id).select_related('category').order_by('-id')
    username = request.session.get('username', '')

    return render(request, 'my_goods.html', {
        'goods_list': goods_list,
        'username': username
    })