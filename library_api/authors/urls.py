from django.urls import path
from .views import AuthorListCreateView, AuthorRetrieveUpdateDestroyView

urlpatterns = [
    path('authors', AuthorListCreateView.as_view(), name='authors'),  # List all authors or create a new author
    path('authors/<int:pk>', AuthorRetrieveUpdateDestroyView.as_view(), name='author-detail'),  # Retrieve, update, or delete an author
]

