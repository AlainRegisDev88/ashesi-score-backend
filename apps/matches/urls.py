from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VenueViewSet, MatchViewSet, MatchClockViewSet, 
    MatchReporterViewSet, LineupEntryViewSet, MatchEventViewSet
)

router = DefaultRouter()
router.register(r'venues', VenueViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'clocks', MatchClockViewSet)
router.register(r'reporters', MatchReporterViewSet)
router.register(r'lineups', LineupEntryViewSet)
router.register(r'events', MatchEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]