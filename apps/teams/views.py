from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Team, Manager, Player, SquadMembership
from .serializers import TeamSerializer, ManagerSerializer, PlayerSerializer, SquadMembershipSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['sport', 'is_active']
    lookup_field = 'slug'

class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['team']

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['is_active']
    lookup_field = 'slug'

class SquadMembershipViewSet(viewsets.ModelViewSet):
    queryset = SquadMembership.objects.all()
    serializer_class = SquadMembershipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['team', 'player', 'sport']