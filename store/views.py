from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Book, Category, Favorite
from .forms import ReviewForm


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

    user_review = None
    review_form = None

    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        if not user_review:
            review_form = ReviewForm()

    if request.method == 'POST' and request.user.is_authenticated:
        if user_review:
            messages.warning(request, "Siz allaqachon sharh qoldirdingiz!")
            return redirect('book_detail', slug=slug)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, "Sharh muvaffaqiyatli qo'shildi!")
            return redirect('book_detail', slug=slug)
        else:
            review_form = form

    context = {
        'book': book,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'related_books': related_books,
        'review_form': review_form,
        'user_review': user_review,
    }
    return render(request, 'store/book_detail.html', context)


@login_required
def toggle_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    favorite = Favorite.objects.filter(
        user=request.user,
        book=book
    ).first()

    if favorite:
        favorite.delete()
        messages.info(request, f'"{book.title}" sevimlilardan olib tashlandi')
    else:
        Favorite.objects.create(user=request.user, book=book)
        messages.success(request, f'"{book.title}" sevimlilarga qo\'shildi!')

    next_url = request.GET.get('next', 'book_detail')
    if next_url == 'book_detail':
        return redirect('book_detail', slug=book.slug)
    return redirect('favorites')


@login_required
def favorites(request):
    favorite_books = Favorite.objects.filter(
        user=request.user
    ).select_related('book')
    return render(request, 'store/favorites.html', {
        'favorite_books': favorite_books
    })