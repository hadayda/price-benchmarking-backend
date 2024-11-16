import django.contrib.admin
from . import  models

@django.contrib.admin.register(models.User)
class UserAdmin(django.contrib.admin.ModelAdmin):
    pass
