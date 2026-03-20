from django.shortcuts import render, redirect
from .models import MarketUser


def register_view(request):
    message = ''

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if MarketUser.objects.filter(username=username).exists():
            message = '用户名已存在'
        else:
            MarketUser.objects.create(
                username=username,
                email=email,
                password=password
            )
            return redirect('/users/login/')

    return render(request, 'register.html', {'message': message})


def login_view(request):
    message = ''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = MarketUser.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return redirect('/goods/list/')
        except MarketUser.DoesNotExist:
            message = '用户名或密码错误'

    return render(request, 'login.html', {'message': message})


def logout_view(request):
    request.session.flush()
    return redirect('/users/login/')