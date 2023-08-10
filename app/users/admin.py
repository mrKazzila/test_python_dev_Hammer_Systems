from django.contrib import admin

from .models import ActivationCode, User

admin.site.register(User)
admin.site.register(ActivationCode)
