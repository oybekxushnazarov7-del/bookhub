from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Category, Author, Book, Review, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'slug', 'birth_date']
    prepopulated_fields = {'slug': ('full_name',)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'stock', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['title', 'author__full_name']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['price', 'stock', 'is_available']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'created_at']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'added_at']