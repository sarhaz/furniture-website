from django.db import models
from django.contrib.auth.models import User
from .helpers import Helpers, PriceType


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    price_type = models.CharField(max_length=100, choices=PriceType.choices, default=PriceType.USA)
    description = models.TextField()
    image = models.ImageField(upload_to=Helpers.product_images)

    def __str__(self):
        return self.name


class Team(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to=Helpers.team_images)
    description = models.TextField()

    def __str__(self):
        return self.first_name


class Comments(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=Helpers.comments_images)

    def __str__(self):
        return self.text[:35]


class Blog(models.Model):
    comments = models.ForeignKey(Comments, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=Helpers.blog_images)

    def __str__(self):
        return self.title[:35]


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product)

