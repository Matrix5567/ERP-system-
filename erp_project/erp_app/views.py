from django.shortcuts import render
from . models import CustomUser
# Create your views here.


def home(request):           # login page / home page
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('full_name')
        image = request.FILES.get('image')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        CustomUser.objects.create_user(full_name=name,email=email, image=image,
                                       password=password2)
        return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')