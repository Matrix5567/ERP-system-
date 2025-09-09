from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from . models import CustomUser
from . validators import name_validator , image_validator , email_validator , password_validator
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):           # login page / home page
    if request.method == 'POST':
        login_email = request.POST.get('email')
        login_password = request.POST.get('password')
        user = authenticate(request, email=login_email, password=login_password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid Login Credentials'})
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect(home)

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

@login_required()
def dashboard(request):
    return render(request,'dashboard.html')