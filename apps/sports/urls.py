from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SportViewSet, PositionViewSet, EventTypeViewSet

router = DefaultRouter()
router.register(r'sports', SportViewSet, basename='sport')
router.register(r'positions', PositionViewSet, basename='position')
router.register(r'event-types', EventTypeViewSet, basename='eventtype')

urlpatterns = [
    path('', include(router.urls)),
]