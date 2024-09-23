from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book, FavoriteBook
from .serializers import BookSerializer, FavoriteBookSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        query = self.request.query_params.get('search')
        if not query:
            return self.queryset
            
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
        
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
       

    def delete(self, request, book_id):
        favorite = FavoriteBook.objects.filter(user=request.user, book_id=book_id).first()
        if not favorite:
            return Response({'error': 'Favorite not found'}, status=status.HTTP_404_NOT_FOUND)
        
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        


class RecommendBooksView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_favorites = FavoriteBook.objects.filter(user=request.user)
        favorite_titles = [fav.book.title for fav in user_favorites]
        recommended_books = Book.objects.exclude(title__in=favorite_titles)[:5]
        serializer = BookSerializer(recommended_books, many=True)
        return Response(serializer.data)
