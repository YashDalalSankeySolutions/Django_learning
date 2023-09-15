from django.db import models

# Create your models here.
class booking(models.Model):
    ticket_id=models.CharField(max_length=10,primary_key=True)
    trip_id=models.CharField(max_length=10)
    user_id=models.CharField(max_length=10)
    traveller_name = models.CharField(max_length=30)
    traveller_number = models.PositiveBigIntegerField(default=0)
    ticket_cost = models.PositiveIntegerField(default=0)
    traveller_email=models.EmailField(max_length=254)