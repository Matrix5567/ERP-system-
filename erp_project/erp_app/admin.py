from django.contrib import admin
from .models import CustomUser , Workspace, Membership
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Workspace)
admin.site.register(Membership)

