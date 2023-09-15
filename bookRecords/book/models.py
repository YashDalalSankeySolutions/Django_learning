from django.db import models
import datetime
# Create your models here.
class Book(models.Model):
    book_name = models.CharField(max_length=30)
    book_quantity = models.PositiveIntegerField()
    book_genre = models.CharField(max_length=30)
    is_best_seller = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

