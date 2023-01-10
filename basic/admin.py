from django.contrib import admin
from django.contrib.auth.models import Group, User

from basic import models

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(models.Product)
admin.site.register(models.Category)
