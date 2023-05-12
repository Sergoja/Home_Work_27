from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=200)
    is_published = models.BooleanField()

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
