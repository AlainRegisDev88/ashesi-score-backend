from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompetitionViewSet,
    CompetitionTeamViewSet,
    RankingRuleViewSet,
    CompetitionStageViewSet,
    StageGroupViewSet,
    StageGroupTeamViewSet,
    KnockoutTieViewSet,
)

router = DefaultRouter()
router.register(r'competitions', CompetitionViewSet)
router.register(r'competition-teams', CompetitionTeamViewSet)
router.register(r'ranking-rules', RankingRuleViewSet)
router.register(r'stages', CompetitionStageViewSet)
router.register(r'stage-groups', StageGroupViewSet)
router.register(r'stage-group-teams', StageGroupTeamViewSet)
router.register(r'knockout-ties', KnockoutTieViewSet)

urlpatterns = [
    path('', include(router.urls)),
]