from django.http import HttpResponse

def aboutUs(request):
    return HttpResponse("This is about page")

def post(request,postId):
    return HttpResponse([postId])
