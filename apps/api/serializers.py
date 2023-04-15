from rest_framework import serializers

from apps.articles.models import Article


class ArticlesSerializer(serializers.ModelSerializer):

    category = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "description",
            "image_url",
            'published_at',
        ]
        read_only = True
