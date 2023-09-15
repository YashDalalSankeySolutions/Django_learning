from django.urls import path,include
from . import views
urlpatterns = [
    path('add',views.book_trip),
    path('list',views.bookingList),
    path('details',views.BookingDetails)
]
