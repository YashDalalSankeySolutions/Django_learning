from django.db import models
from route import models as route_model
# Create your models here.
class trips(models.Model):
    trip_id=models.CharField(max_length=10,primary_key=True)
    user_id=models.CharField(max_length=10)
    vehicle_id=models.CharField(max_length=10)
    route_id=models.ForeignKey(route_model.route, on_delete=models.CASCADE)
    driver_name = models.CharField(max_length=30)
    trip_distance = models.PositiveSmallIntegerField(default=0)
    
