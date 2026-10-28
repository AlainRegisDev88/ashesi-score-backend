from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import NewsArticle, Award
from .serializers import NewsArticleSerializer, AwardSerializer

class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['sport', 'status']
    lookup_field = 'slug'

class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['award_type', 'competition', 'match', 'player', 'team']