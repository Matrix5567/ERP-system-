from django.shortcuts import render, redirect
from . models import CustomUser
from . validators import name_validator , image_validator , email_validator , password_validator
from django.contrib.auth.hashers import check_password
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
        name_error = name_validator(name)
        image_error = image_validator(image)
        email_error = email_validator(email)
        password_error = password_validator(password1,password2)
        errors ={}
        if name_error:
            errors['name'] = name_error
        if email_error:
            errors['email'] = email_error
        if image_error:
            errors['image'] = image_error
        if password_error:
            errors['password'] = password_error
        if errors:
            return render(request, 'signup.html',{'error':errors})
        else:
            CustomUser.objects.create_user(full_name=name,email=email, image=image,
                                       password=password2)
            return redirect('home')
    else:
        return render(request, 'signup.html')