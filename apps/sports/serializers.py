from rest_framework import serializers
from .models import Sport, Position, EventType

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = [
            'id', 'name', 'slug', 'clock_direction', 'period_label', 
            'starters_count', 'coverage_tier', 'period_length_minutes', 
            'periods_count', 'stoppage_time_enabled', 'extra_time_enabled', 
            'shootout_enabled', 'is_active'
        ]

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'sport', 'name', 'code']

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ['id', 'sport', 'name', 'code', 'points', 'related_player_role', 'is_shootout', 'is_active']