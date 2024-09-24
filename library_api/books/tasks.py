# books/tasks.py
from celery import shared_task
from django.core.cache import cache
from .models import Book, FavoriteBook
from .serializers import BookSerializer

@shared_task
def update_recommendations(user_id):

    from django.contrib.auth.models import User
    user = User.objects.get(pk=user_id)

    user_favorites = FavoriteBook.objects.filter(user=user).values_list('book_id', flat=True)
    recommended_books = Book.objects.exclude(id__in=user_favorites).order_by('-popularity')[:5]
    recommendations = BookSerializer(recommended_books, many=True).data
    cache.set(f"user_{user.id}_recommendations", recommendations, timeout=60 * 60 * 24)  # Cache for a day
