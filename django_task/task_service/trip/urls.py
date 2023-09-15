from django.urls import path
from . import views
urlpatterns = [
    path('add',views.add_trip),
    path('list',views.trip_list),
    path('details',views.trip_details)
]