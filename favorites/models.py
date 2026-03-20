from django.db import models
from users.models import MarketUser
from goods.models import Goods


class Favorite(models.Model):
    user = models.ForeignKey(MarketUser, on_delete=models.CASCADE, related_name='favorites', verbose_name='用户')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='favorited_by', verbose_name='商品')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        unique_together = ('user', 'goods')
        verbose_name = '收藏'
        verbose_name_plural = '收藏'

    def __str__(self):
        return f'{self.user.username} 收藏了 {self.goods.title}'