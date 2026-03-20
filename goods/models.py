from django.db import models
from users.models import MarketUser


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='分类名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name


class Goods(models.Model):
    title = models.CharField(max_length=100, verbose_name='商品标题')
    description = models.TextField(verbose_name='商品描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    contact = models.CharField(max_length=50, verbose_name='联系方式')
    user = models.ForeignKey(MarketUser, on_delete=models.CASCADE, verbose_name='发布人', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='商品分类', null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='商品图片')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    def __str__(self):
        return self.title