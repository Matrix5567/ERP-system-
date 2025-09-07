from django.shortcuts import render

# Create your views here.


def home(request):           # login page / home page
    return render (request, 'login.html')