from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class route(models.Model):
    route_id = models.CharField(max_length=10,primary_key=True)
    user_id = models.CharField(max_length=10)
    route_name = models.CharField(max_length=50)
    route_origin = models.CharField(max_length=30)
    route_destination = models.CharField(max_length=30)
    stops = ArrayField(models.CharField(max_length=10))
