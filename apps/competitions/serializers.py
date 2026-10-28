from rest_framework import serializers
from .models import (
    Competition,
    CompetitionTeam,
    RankingRule,
    CompetitionStage,
    StageGroup,
    StageGroupTeam,
    KnockoutTie,
)

class RankingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RankingRule
        fields = ['id', 'priority', 'criterion']


class CompetitionTeamSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = CompetitionTeam
        fields = ['id', 'competition', 'team', 'team_name', 'registered_at']


class StageGroupTeamSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = StageGroupTeam
        fields = ['id', 'group', 'team', 'team_name']


class StageGroupSerializer(serializers.ModelSerializer):
    group_teams = StageGroupTeamSerializer(many=True, read_only=True)

    class Meta:
        model = StageGroup
        fields = ['id', 'stage', 'name', 'group_teams']


class KnockoutTieSerializer(serializers.ModelSerializer):
    home_team_name = serializers.CharField(source='home_team.name', read_only=True, allow_null=True)
    away_team_name = serializers.CharField(source='away_team.name', read_only=True, allow_null=True)
    winner_team_name = serializers.CharField(source='winner_team.name', read_only=True, allow_null=True)

    class Meta:
        model = KnockoutTie
        fields = [
            'id', 'stage', 'slot', 'home_team', 'home_team_name',
            'away_team', 'away_team_name', 'winner_team', 'winner_team_name',
            'advances_to_tie', 'advances_to_slot'
        ]


class CompetitionStageSerializer(serializers.ModelSerializer):
    groups = StageGroupSerializer(many=True, read_only=True)
    knockout_ties = KnockoutTieSerializer(many=True, read_only=True)

    class Meta:
        model = CompetitionStage
        fields = ['id', 'competition', 'name', 'stage_type', 'sequence', 'two_legged', 'groups', 'knockout_ties']


class CompetitionSerializer(serializers.ModelSerializer):
    ranking_rules = RankingRuleSerializer(many=True, read_only=True)
    competition_teams = CompetitionTeamSerializer(many=True, read_only=True)
    stages = CompetitionStageSerializer(many=True, read_only=True)
    sport_name = serializers.CharField(source='sport.name', read_only=True)

    class Meta:
        model = Competition
        fields = [
            'id', 'name', 'sport', 'sport_name', 'competition_type',
            'status', 'start_date', 'end_date', 'points_for_win',
            'points_for_draw', 'ranking_rules', 'competition_teams', 'stages'
        ]