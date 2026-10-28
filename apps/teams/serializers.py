from rest_framework import serializers
from .models import Team, Manager, Player, SquadMembership

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'sport', 'name', 'short_name', 'slug', 'logo', 'is_active']

class ManagerSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Manager
        fields = ['id', 'team', 'team_name', 'first_name', 'last_name', 'photo', 'is_active']

class SquadMembershipSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)
    position_name = serializers.CharField(source='position.name', read_only=True)

    class Meta:
        model = SquadMembership
        fields = ['id', 'player', 'team', 'team_name', 'sport', 'position', 'position_name', 'jersey_number', 'start_date', 'end_date']

class PlayerSerializer(serializers.ModelSerializer):
    current_squads = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['id', 'first_name', 'last_name', 'slug', 'photo', 'is_active', 'current_squads']

    def get_current_squads(self, obj):
        active_squads = obj.squad_memberships.filter(end_date__isnull=True)
        return SquadMembershipSerializer(active_squads, many=True).data