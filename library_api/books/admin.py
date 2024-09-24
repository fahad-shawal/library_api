from django.contrib import admin
from .models import Book, FavoriteBook

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'published_date']
    search_fields = ['title', 'author__name']
    list_filter = ['published_date', 'author']

@admin.register(FavoriteBook)
class FavoriteBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book']
    search_fields = ['user__username', 'book__title']
