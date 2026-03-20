from django.db import models

# Create your models here.
class MarketUser(models.Model):
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    password = models.CharField(max_length=255, verbose_name='密码')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.username