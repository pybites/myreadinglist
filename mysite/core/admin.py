from django.contrib import admin

from .models import Book, Search, Like, Status

admin.site.register(Book)
admin.site.register(Search)
admin.site.register(Like)
admin.site.register(Status)
