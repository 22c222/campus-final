from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='分类名称')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def __str__(self):
        return self.name


class Goods(models.Model):
    title = models.CharField(max_length=200, verbose_name='商品名称')
    description = models.TextField(verbose_name='商品描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    contact = models.CharField(max_length=100, verbose_name='联系方式')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='分类'
    )

    user = models.ForeignKey(
        'users.MarketUser',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='发布用户'
    )

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='商品图片'
    )

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'

    def __str__(self):
        return self.title