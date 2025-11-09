from django.contrib.auth.models import User
from django.db import models
import os
from datetime import datetime
from django.utils.text import slugify
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=150)  # Назва продукту
    description = models.TextField(blank=True)  # Детальний опис
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Ціна
    image = models.ImageField(upload_to='products/', blank=True)  # Зображення
    is_available = models.BooleanField(default=True)  # Чи доступний товар
    created_at = models.DateTimeField(auto_now_add=True)  # Дата створення
    modified_at = models.DateTimeField(auto_now=True) # Дата останньої зміни
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name = 'Категорія'
    )
    def __str__(self) -> str:
        return str(self.name)



class Category(models.Model):
    name = models.CharField('Назва', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField('Опис', blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Батьківська категорія'
    )
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['name']

    def __str__(self):
        return self.name





