from rest_framework import serializers
from .models import NewsArticle, Award

class NewsArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = NewsArticle
        fields = ['id', 'sport', 'author', 'author_name', 'title', 'slug', 'body', 'cover_image', 'status', 'published_at']

class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ['id', 'title', 'award_type', 'competition', 'match', 'player', 'team', 'description', 'awarded_by', 'created_at']