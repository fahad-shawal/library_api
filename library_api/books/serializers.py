from rest_framework import serializers
from .models import Book, FavoriteBook
from authors.serializers import AuthorSerializer

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = '__all__'


class FavoriteBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteBook
        fields = ['book']
