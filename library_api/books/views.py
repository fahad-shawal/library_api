from django.core.cache import cache
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book, FavoriteBook
from .serializers import BookSerializer, FavoriteBookSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .tasks import update_recommendations
from .utils import calculate_recommendations 


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        query = self.request.query_params.get('search')
        if not query:
            return self.queryset.all()
            
        return self.queryset.filter(Q(title__icontains=query) | Q(author__name__icontains=query))

    def perform_create(self, serializer):
        serializer.save()


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs['pk'])
        serializer = self.serializer_class(book, data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def delete(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs['pk'])
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FavoriteBookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        favorite = serializer.save(user=request.user)
        update_recommendations.delay(request.user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

    def delete(self, request, book_id):
        favorite = FavoriteBook.objects.filter(user=request.user, book_id=book_id).first()
        if not favorite:
            return Response({'error': 'Favorite not found'}, status=status.HTTP_404_NOT_FOUND)
        
        favorite.delete()
        update_recommendations.delay(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
class RecommendBooksView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        cache_key = f"user_{user.id}_recommendations"
        recommendations = cache.get(cache_key)

        if recommendations is None:
            # Fallback if recommendations are not available in the cache
            recommendations = calculate_recommendations(user)
            # Cache the recommendations to optimize future requests
            cache.set(cache_key, recommendations, timeout=60 * 5)  # Cache for 5 minutes

        return Response(recommendations)
