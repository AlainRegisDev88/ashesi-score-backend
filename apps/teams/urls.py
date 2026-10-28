from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, ManagerViewSet, PlayerViewSet, SquadMembershipViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'managers', ManagerViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'squads', SquadMembershipViewSet)

urlpatterns = [
    path('', include(router.urls)),
]