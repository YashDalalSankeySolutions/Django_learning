from django.urls import path,include
from . import views
urlpatterns = [
    path('list', views.bookDetails),
    path('add', views.addBook),
    path('<id>', views.book)
]