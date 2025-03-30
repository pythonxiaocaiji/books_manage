from rest_framework import serializers

from Apps.books.models import Books


class BooksSerializer(serializers.ModelSerializer):
    lending_user_name = serializers.CharField(source='lending_user.name', read_only=True)

    class Meta:
        model = Books
        fields = '__all__'
        extra_kwargs = {
            'lending_user': {'write_only': True},
        }