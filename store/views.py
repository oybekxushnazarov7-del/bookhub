from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Avg
from .models import Book, Category, Author


def home(request):
    featured_books = Book.objects.filter(is_available=True)[:8]
    categories = Category.objects.all()
    context = {
        'featured_books': featured_books,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)


def book_list(request):
    books = Book.objects.filter(is_available=True)
    categories = Category.objects.all()

    # Qidiruv
    query = request.GET.get('q')
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__full_name__icontains=query) |
            Q(description__icontains=query)
        )

    # Kategoriya filtri
    category_slug = request.GET.get('category')
    if category_slug:
        books = books.filter(category__slug=category_slug)

    context = {
        'books': books,
        'categories': categories,
        'query': query,
    }
    return render(request, 'store/book_list.html', context)


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    reviews = book.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    related_books = Book.objects.filter(
        category=book.category
    ).exclude(id=book.id)[:4]

    context = {
        'book': book,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'related_books': related_books,
    }
    return render(request, 'store/book_detail.html', context)