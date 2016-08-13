from django.contrib import admin
from .models import Logger
from django.utils.safestring import mark_safe

#Let Django know about the app
admin.site.register(Logger)

