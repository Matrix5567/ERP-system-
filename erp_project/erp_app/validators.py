from . models import CustomUser, Workspace
import imghdr
import re

def name_validator(name):
    if not name:
        return "Name cannot be empty"
    else :
        if len(name)<2:
            return "Name must be greater than three digits"
        else:
            return None

def image_validator(image):
    if not image:
        return "Image cannot be empty"
    else:
        if image.size > 5 * 1024 * 1024:  # 5MB limit
            return "Image file size must be less than 5MB."

        ext = image.name.split('.')[-1].lower()
        if ext not in ['jpg', 'jpeg']:
            return "Only JPEG images are allowed."

    # Extra check to ensure it's a real JPEG file
        if imghdr.what(image) not in ['jpeg']:
            return "Invalid image format. Only JPEG is allowed."
        return None

def email_validator(email):
    if not email:
        return "Email cannot be empty"
    elif CustomUser.objects.filter(email=email).exists():
        return "This email already exists"
    else:
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-,]+$",email):
            return "Invalid Email"
        else:
            return None

def password_validator(password1 , password2):
    if not password1 and not password2:
        return "Password cannot be empty"
    else:
        if password1 != password2:
            return "Passwords do not match"
        if not re.match(r"^(?=.*[!@#$%^&*()_+{}:;\"'<>,.?/~`-]).{5,}$", password2):
            return "Password must be atleast 5 long and must have one special characters"
        else:
            return None

def workspace_name_validator(name,request):
    if not name:
        return "Workspace name cannot be empty"
    else:
        if len(name)<3:
            return "Workspace name must be greater than three letters"
        if Workspace.objects.filter(name=name,created_by=request.user).exists():
            return "Workspace with this name already exists"





