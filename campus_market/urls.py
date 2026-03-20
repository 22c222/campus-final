from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


def home(request):
    return redirect('/goods/list/')


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('goods/', include('goods.urls')),
    path('users/', include('users.urls')),
    path('comments/', include('comments.urls')),
    path('favorites/', include('favorites.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)