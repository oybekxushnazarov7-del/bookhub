from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorite/toggle/<int:book_id>/', views.toggle_favorite, name='toggle_favorite'),
]