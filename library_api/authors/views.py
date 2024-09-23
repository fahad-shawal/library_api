# authors/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Author
from .serializers import AuthorSerializer
from django.shortcuts import get_object_or_404


class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class AuthorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, *args, **kwargs):
        author = get_object_or_404(Author, pk=kwargs['pk'])
        serializer = self.serializer_class(author, data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
       

    def delete(self, request, *args, **kwargs):
        author = get_object_or_404(Author, pk=kwargs['pk'])
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
