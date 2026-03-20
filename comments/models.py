from django.db import models
from goods.models import Goods
from users.models import MarketUser


class Comment(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='comments', verbose_name='所属商品')
    user = models.ForeignKey(MarketUser, on_delete=models.CASCADE, related_name='comments', verbose_name='评论用户')
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    def __str__(self):
        return f'{self.user.username} - {self.goods.title}'