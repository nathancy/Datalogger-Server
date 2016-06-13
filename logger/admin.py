from django.contrib import admin
from .models import Logger
from django.utils.safestring import mark_safe

admin.site.register(Logger)

