from django.db import models
# Create your models here.

class Books(models.Model):
    book_name=models.CharField(max_length=40)
    book_quantity=models.IntegerField()
    book_genre= models.CharField(max_length=30)


