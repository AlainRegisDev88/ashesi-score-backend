from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Venue, Match, MatchClock, MatchReporter, LineupEntry, MatchEvent
from .serializers import (
    VenueSerializer, MatchSerializer, MatchClockSerializer, 
    MatchReporterSerializer, LineupEntrySerializer, MatchEventSerializer
)

class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['sport', 'competition', 'status', 'venue']

class MatchClockViewSet(viewsets.ModelViewSet):
    queryset = MatchClock.objects.all()
    serializer_class = MatchClockSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['match']

class MatchReporterViewSet(viewsets.ModelViewSet):
    queryset = MatchReporter.objects.all()
    serializer_class = MatchReporterSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['match', 'user']

class LineupEntryViewSet(viewsets.ModelViewSet):
    queryset = LineupEntry.objects.all()
    serializer_class = LineupEntrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['match', 'team', 'is_starter']

class MatchEventViewSet(viewsets.ModelViewSet):
    queryset = MatchEvent.objects.all()
    serializer_class = MatchEventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['match', 'team', 'event_type', 'is_voided']