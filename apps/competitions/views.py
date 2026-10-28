from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import (
    Competition,
    CompetitionTeam,
    RankingRule,
    CompetitionStage,
    StageGroup,
    StageGroupTeam,
    KnockoutTie,
)
from .serializers import (
    CompetitionSerializer,
    CompetitionTeamSerializer,
    RankingRuleSerializer,
    CompetitionStageSerializer,
    StageGroupSerializer,
    StageGroupTeamSerializer,
    KnockoutTieSerializer,
)

class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['sport', 'competition_type', 'status']


class CompetitionTeamViewSet(viewsets.ModelViewSet):
    queryset = CompetitionTeam.objects.all()
    serializer_class = CompetitionTeamSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['competition', 'team']


class RankingRuleViewSet(viewsets.ModelViewSet):
    queryset = RankingRule.objects.all()
    serializer_class = RankingRuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['competition']


class CompetitionStageViewSet(viewsets.ModelViewSet):
    queryset = CompetitionStage.objects.all()
    serializer_class = CompetitionStageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['competition', 'stage_type']


class StageGroupViewSet(viewsets.ModelViewSet):
    queryset = StageGroup.objects.all()
    serializer_class = StageGroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['stage']


class StageGroupTeamViewSet(viewsets.ModelViewSet):
    queryset = StageGroupTeam.objects.all()
    serializer_class = StageGroupTeamSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['group', 'team']


class KnockoutTieViewSet(viewsets.ModelViewSet):
    queryset = KnockoutTie.objects.all()
    serializer_class = KnockoutTieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['stage']