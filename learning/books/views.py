from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Books
from django.core import serializers
import json

# Create your views here.
def bookDetails(request):
    # print("-------------------------")
    # print(request.method)
    data = Books.objects.all()
    data_json = serializers.serialize('json', data)
    return HttpResponse(data_json,content_type='application/json')

def getBook(request,id):
    print("-----------------")
    print(request.method)
    data = Books.objects.filter(id =id).values()
    return HttpResponse(data,content_type='application/json')

def addBook(request):
    print("--------------")
    data = json.loads(request.body)
    booksObject = Books()
    booksObject.book_name = data["name"]
    booksObject.book_quantity = data["quantity"]
    booksObject.book_genre = data["genre"]

    return HttpResponse("huuu")




