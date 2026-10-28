from rest_framework import serializers
from .models import Venue, Match, MatchClock, MatchReporter, LineupEntry, MatchEvent

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name', 'description', 'capacity', 'photo']

class MatchClockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchClock
        fields = ['id', 'match', 'period_label', 'clock_seconds', 'is_running', 'stoppage_seconds', 'updated_at']

class MatchReporterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = MatchReporter
        fields = ['id', 'match', 'user', 'username', 'assigned_at']

class LineupEntrySerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.name', read_only=True)
    position_name = serializers.CharField(source='position.name', read_only=True)

    class Meta:
        model = LineupEntry
        fields = ['id', 'match', 'team', 'player', 'player_name', 'position', 'position_name', 'jersey_number', 'is_starter']

class MatchEventSerializer(serializers.ModelSerializer):
    event_type_name = serializers.CharField(source='event_type.name', read_only=True)
    player_name = serializers.CharField(source='player.name', read_only=True)
    related_player_name = serializers.CharField(source='related_player.name', read_only=True, allow_null=True)

    class Meta:
        model = MatchEvent
        fields = [
            'id', 'match', 'event_type', 'event_type_name', 'team',
            'player', 'player_name', 'related_player', 'related_player_name',
            'period', 'clock_seconds', 'stoppage_offset_seconds', 'is_voided', 'created_at'
        ]

class MatchSerializer(serializers.ModelSerializer):
    home_team_name = serializers.CharField(source='home_team.name', read_only=True)
    away_team_name = serializers.CharField(source='away_team.name', read_only=True)
    venue_name = serializers.CharField(source='venue.name', read_only=True)
    sport_name = serializers.CharField(source='sport.name', read_only=True)
    
    clock = MatchClockSerializer(read_only=True)
    reporters = MatchReporterSerializer(many=True, read_only=True)
    lineups = LineupEntrySerializer(many=True, read_only=True)
    events = MatchEventSerializer(many=True, read_only=True)

    class Meta:
        model = Match
        fields = [
            'id', 'sport', 'sport_name', 'competition', 'stage', 'group', 'knockout_tie', 'leg_number',
            'home_team', 'home_team_name', 'away_team', 'away_team_name',
            'venue', 'venue_name', 'scheduled_at', 'status',
            'home_score', 'away_score', 'home_shootout_score', 'away_shootout_score',
            'coverage_tier', 'clock', 'reporters', 'lineups', 'events'
        ]