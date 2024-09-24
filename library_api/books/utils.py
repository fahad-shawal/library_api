# books/utils.py
from .models import Book, FavoriteBook
from .serializers import BookSerializer


def calculate_recommendations(user):
    """
    Calculate book recommendations based on the user's favorite books.
    This function will be used as a fallback when recommendations are not cached.
    """
    user_favorites = FavoriteBook.objects.filter(user=user).values_list('book_id', flat=True)
    recommended_books = Book.objects.exclude(id__in=user_favorites).order_by('-popularity')[:5]
    recommendations = BookSerializer(recommended_books, many=True).data

    return recommendations
