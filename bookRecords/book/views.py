from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from .models import Book
import json
# Create your views here.
def bookDetails(request):
    data = Book.objects.all()
    data_json = serializers.serialize('json',data)
    return HttpResponse(data_json,"application/json")

def addBook(request):
    data = json.loads(request.body)
    bookObject = Book()
    bookObject.book_name = data['name']
    bookObject.book_quantity = data['quantity']
    bookObject.book_genre = data['genre']
    bookObject.is_best_seller = data['is_best_seller']
    bookObject.save()
    return JsonResponse({"message":"Data Added Successfully"})

def book(request,id):
    try:
        book = Book.objects.get(id=id)
    except:
        return JsonResponse({"message":"Invalid Request"},status =400)
    if(request.method=="GET"):
        print("------------------------------")
        content={
            "id":book.id,
            "book_quantity":book.book_quantity,
            "book_genre":book.book_genre,
            "is_best_seller":book.is_best_seller,
            "created_at":book.created_at,
            "updated_at":book.updated_at
        }
        print(content)
        return JsonResponse(content)
    elif(request.method=="PUT"):
        print("------------------------------")
        data = json.loads(request.body)
        book.book_name = data['name']
        book.book_quantity = data['quantity']
        book.book_genre = data['genre']
        book.is_best_seller = data['is_best_seller']
        book.save()
        return JsonResponse({"message":"Data update Successfully"})
    elif(request.method=="DELETE"):
        book.delete()
        return JsonResponse({"message":"Data deleted Successfully"})
    return JsonResponse({"message":"Invalid Api Call"})



