from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsArticleViewSet, AwardViewSet

router = DefaultRouter()
router.register(r'news', NewsArticleViewSet)
router.register(r'awards', AwardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]