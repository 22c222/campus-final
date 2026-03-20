from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Goods(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    contact = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('users.MarketUser', on_delete=models.CASCADE, null=True, blank=True)

    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField("图片链接", max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title