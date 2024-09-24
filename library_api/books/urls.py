from django.urls import path
from .views import (
    BookListCreateView, BookRetrieveUpdateDestroyView,
    FavoriteBookView, RecommendBooksView
)

urlpatterns = [
    path('', BookListCreateView.as_view(), name='books'),
    path('<int:pk>', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
    path('favorites', FavoriteBookView.as_view(), name='favorites'),
    path('recommendations', RecommendBooksView.as_view(), name='recommendations'),
]