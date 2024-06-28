import uuid
from django.db import models


class PriceType(models.TextChoices):
    USA = '$', '$'
    EURO = 'EU', 'EU'
    SUM = 'SUM', 'SUM'


class Helpers(models.Model):
    def product_images(instance, filename):
        image_ext = filename.split('.')[-1]
        return f'products/{uuid.uuid4()}.{image_ext}'

    def team_images(instance, filename):
        image_ext = filename.split('.')[-1]
        return f'team/{uuid.uuid4()}.{image_ext}'

    def comments_images(instance, filename):
        image_ext = filename.split('.')[-1]
        return f'comments/{uuid.uuid4()}.{image_ext}'

    def blog_images(instance, filename):
        image_ext = filename.split('.')[-1]
        return f'blog/{uuid.uuid4()}.{image_ext}'



